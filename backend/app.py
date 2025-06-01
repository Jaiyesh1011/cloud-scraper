from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
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

@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        url = 'http://books.toscrape.com/'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        books = []

        for item in soup.select('.product_pod'):
            title = item.h3.a['title']
            price = item.select_one('.price_color').text
            stock = item.select_one('.availability').text.strip()
            books.append({'title': title, 'price': price, 'stock': stock})

        collection.delete_many({})
        collection.insert_many(books)
        return jsonify({"message": "Scraped and saved!"}), 200

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
