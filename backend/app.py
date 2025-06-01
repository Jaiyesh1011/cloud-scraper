from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask import request 
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient(os.environ["MONGO_URI"])
db = client["scraper"]
collection = db["books"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend is running"}), 200

 # Add this at top

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url", "https://books.toscrape.com/")  # default fallback
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        scraped_data = []
        books = soup.select("article.product_pod")
        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            stock = book.select_one(".instock.availability").text.strip()
            scraped_data.append({
                "title": title,
                "price": price,
                "stock": stock
            })

        collection.delete_many({})  # optional: clean old data
        collection.insert_many(scraped_data)
        return jsonify({"status": "success", "data": scraped_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/books', methods=['GET'])
def get_books():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
