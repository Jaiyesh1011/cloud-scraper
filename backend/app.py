from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

client = MongoClient(os.environ["MONGO_URI"])
db = client["scraper"]
collection = db["books"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend is running"}), 200

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        url = data.get("url", "http://books.toscrape.com")  # Default if not provided

        res = requests.get(url, timeout=10)
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

        collection.delete_many({})
        collection.insert_many(books)

        return jsonify({"status": "success", "data": books}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "data": []}), 500

@app.route('/books', methods=['GET'])
def get_books():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "data": []}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
