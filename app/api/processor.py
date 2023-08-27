from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.sentiment.Sentiment import roberta_polarity_score
import string
# from . import processor_bp

processor_bp = Blueprint('processor', __name__)

threshold = 45

def clean_text(text, stopwords):
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('','', string.punctuation)) # remove punctuations
    tokenized_words = cleaned_text.split()

    clear_text = []
    for word in tokenized_words:
        if word not in stopwords:
            clear_text.append(word)
    
    return clear_text

# get neg to pos ratio
def findRatio(text):
    neg = roberta_polarity_score(text)['neg']
    pos = roberta_polarity_score(text)['pos']
    return int(neg / pos)

# check last searches
def getScore(last_searches):
    total = 0
    for text in last_searches:
        roberta_result = findRatio(text)
        total += roberta_result
    return total

#check new_search
file = ['abuse','abused','abusement','assault','assaulted','catastrophe','crisis','death','pain','panic','suicide','trauma','disaster','hurt','painful','victim','violence','anxiety','hurting','anxious','painfully','depression','depressed']

def checkExtreme(text):
    if findRatio(text) < threshold:
        for word in file:
            if word == text:
                return True
        return False
    return True

def stressAnalyzer(clear_text, last_searches):
    score = 0
    message = ""
    extremeFlag = False
    for word in clear_text:
        if checkExtreme(text = word):
            extremeFlag = True

    if getScore(last_searches) >= threshold or extremeFlag:
        message = "Are you not feeling well?"
        score = -1
    
    return message, score 

@processor_bp.route('/processSearchData', methods=['POST'])
def process():
    stopwords = ['google', 'search', 'emotions']
    try: 
        data_received = request.json
        print (data_received)
        if 'new_search' in data_received and 'last_searches' in data_received:
            new_search = data_received['new_search']
            last_searches = data_received['last_searches']
            # print(new_search)
            clear_text = clean_text(new_search, stopwords)

            message, score = stressAnalyzer(clear_text, last_searches)

            response = { 'clear_search' : clear_text, 'message' : message, 'score' : score } 
            print(response)    
            return jsonify(response), 200       
        else: 
            return jsonify({'Error': str(e)}), 400
        
    except Exception as e:
        print(str(e))
        return jsonify({'Error': str(e)}), 500
