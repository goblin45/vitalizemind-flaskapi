from googleapiclient.discovery import build
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import requests
from langdetect import detect
from app.emotions.EmoMusicDict import get_keywords
from app.emotions.api_keys import my_api_key

music_bp = Blueprint('music', __name__)
CORS(music_bp, resources={r"/*": {"origins": { "https://vitalizemind-nodeapi.onrender.com" } }})

@music_bp.route('/getMusics', methods = ['POST'])
def search_musics():
    data_received = request.json
    preferences = []
    keywords = []

    if 'preferences' in data_received:
        preferences = data_received['preferences']
    if 'current_emotion' in data_received:
        current_emotion = data_received['current_emotion'].lower()
        keywords = get_keywords(current_emotion)

    # build the q
    keywords_str = ""
    preferences_str = ""
    for keyword in keywords:
        if (len(keywords_str) > 0):
            keywords_str += "|"
        keywords_str += keyword
    for preference in preferences:
        if (len(preferences_str) > 0):
            preferences_str += "|"
        preferences_str += preference

    youtube = build('youtube', 'v3', developerKey = my_api_key)

    musicsToShow = []

    try:
        next_page_token = ""
        filter_str = keywords_str

        while (len(musicsToShow) < 6):      
            print(filter_str)          

            search_response = youtube.search().list(
                part = 'snippet',
                q = filter_str,
                maxResults = 10,
                safeSearch = 'strict',
                type = 'video',
                videoDefinition = 'high',
                videoDuration = 'medium',
                videoCategoryId = '10',
                pageToken = next_page_token
            ).execute()

            if 'items' in search_response:
                for music in search_response['items']:
                    music_id = music['id']['videoId']
                    music_title = music['snippet']['title']
                    try:
                        titleLang = detect(music_title)
                        if titleLang == 'en':
                            if len(musicsToShow) == 4 and filter_str != preferences_str:
                                filter_str = preferences_str
                                next_page_token = ""
                                break
                            if len(musicsToShow) < 6:
                                musicsToShow.append(music_id)
                                print("passed: " + music_id + " " + music_title)
                            else:
                                break
                        else:
                            pass
                    except Exception as e:
                        pass
                    
            next_page_token = search_response.get('nextPageToken')
                
    except Exception as e:
        print('Error' + str(e))
        return jsonify({ 'error' : str(e) }), 500

    for music in musicsToShow:
        print(music)

    return jsonify({ 'musicIds' : musicsToShow }), 200