import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env') 
load_dotenv(dotenv_path) 

MONGODB_URI = os.environ.get("MONGODB_URI") 
DB_NAME = os.environ.get("DB_NAME") 

client = MongoClient(MONGODB_URI) 
db = client[DB_NAME] 
collection = db['articles']

app = Flask(__name__)

@app.route('/')
def index():
    articles = collection.find()
    return render_template('index.html', articles=articles)

@app.route('/add', methods=['POST'])
def add_article():
    data = request.get_json()
    title = data.get('title')  
    content = data.get('content')
    article_id = collection.insert_one({'title': title, 'content': content}).inserted_id

    return jsonify({
        '_id': str(article_id),
        'title': title,
        'content': content
    })

@app.route('/article/<id>')
def article(id):
    article = collection.find_one({'_id': ObjectId(id)})
    return render_template('article.html', article=article)

@app.route('/update/<id>', methods=['POST'])
def update_article(id):
    new_title = request.form.get('new_title')
    new_content = request.form.get('new_content')
    collection.update_one({'_id': ObjectId(id)}, {'$set': {'title': new_title, 'content': new_content}})

    return jsonify({
        '_id': id,
        'title': new_title,
        'content': new_content
    })

@app.route('/delete/<id>', methods=['DELETE'])
def delete_article(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'_id': id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
