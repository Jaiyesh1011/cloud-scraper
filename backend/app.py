from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os



app = Flask(__name__)
CORS(app, resources={r"/books": {"origins": "https://cloud-scraper.vercel.app"}})


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
        url = data.get("url", "http://books.toscrape.com") 

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

@app.route("/books", methods=["GET"])
def get_books():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    skip = (page - 1) * page_size

    books = list(collection.find().skip(skip).limit(page_size))
    for book in books:
        book['_id'] = str(book['_id'])
    return jsonify(books)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
