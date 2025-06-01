from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Rate limiting to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# MongoDB setup
client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = client["scraper"]
collection = db["books"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend is running"}), 200

@app.route("/scrape", methods=["GET"])
@limiter.limit("10 per hour")  # Prevent excessive scraping
def scrape():
    url = "http://books.toscrape.com"
    try:
        res = requests.get(url, timeout=10)  # Add timeout
        soup = BeautifulSoup(res.text, "html.parser")
        books = []

        for book in soup.select(".product_pod"):
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text.strip()
            stock = book.select_one(".availability").text.strip()
            books.append({
                "title": title,
                "price": price,
                "stock": stock
            })

        # Clear old data & insert new
        collection.delete_many({})
        collection.insert_many(books)

        return jsonify({"status": "success", "count": len(books)}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/books', methods=['GET'])
def get_books():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)