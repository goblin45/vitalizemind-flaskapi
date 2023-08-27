from googleapiclient.discovery import build
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import requests
from langdetect import detect
from app.emotions.EmoBooksDict import get_keywords
from app.emotions.api_keys import my_api_key

books_bp = Blueprint('books', __name__)
CORS(books_bp, resources={r"/*": {"origins": { "https://vitalizemind-nodeapi.onrender.com/content/books" } }})

books = build('books', 'v1', developerKey = my_api_key)

@books_bp.route('/getBooks', methods = ['POST'])
def search_books():
    data_received = request.json
    keywords = []
    preferences = []

    print(data_received)

    if 'preferences' in data_received:
        preferences = data_received['preferences']
    if 'current_emotion' in data_received:
        current_emotion = data_received['current_emotion'].lower()
        
    keywords = get_keywords(current_emotion)

    keywords_str = ""
    preferences_str = ""
    for keyword in keywords:
        if (len(keywords_str) > 0):
            keywords_str += " "
        keywords_str += keyword
    for preference in preferences:
        if (len(preferences_str) > 0):
            preferences_str += " "
        preferences_str += preference

    booksToShow = []
    filter_str = keywords_str
    
    
    while (len(booksToShow) < 6):
        print(filter_str)
        search_response = books.volumes().list(
            q = filter_str,
            maxResults = 10,
            filter = "free-ebooks"
        ).execute()

        if 'items' in search_response:
            for book in search_response['items']:
                book_id = book['id']
                book_name = book['volumeInfo']['title']
                if len(booksToShow) == 4 and filter_str != preferences_str:
                    filter_str = preferences_str
                    break
                if len(booksToShow) < 6:
                    booksToShow.append(book)
                    print("passed: " + book_id + " " + book_name)
                elif len(booksToShow) >= 6:
                    break


    try:            
        return jsonify({ 'books' : booksToShow }), 200
    except Exception as e:
        return jsonify({ 'message' : 'An error occurred: ' + e }), 500