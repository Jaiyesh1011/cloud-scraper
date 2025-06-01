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

@app.route("/scrape", methods=["GET"])
def scrape():
    try:
        # Use a public JSON API (placeholder example)
        res = requests.get("https://fakestoreapi.com/products?limit=5")
        json_data = res.json()

        scraped_data = []
        for item in json_data:
            scraped_data.append({
                "title": item["title"],
                "price": f"${item['price']}",
                "stock": "In Stock"  # Fake API doesn't provide stock info
            })

        # Save to MongoDB
        collection.delete_many({})  # clear old data
        collection.insert_many(scraped_data)

        return jsonify({"status": "success", "count": len(scraped_data)})
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
