from flask import Flask, jsonify
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

@app.route('/scrape', methods=['GET'])
def scrape():
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
    return jsonify({"message": "Scraped and saved!"})

@app.route('/books', methods=['GET'])
def get_books():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run()
