from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import requests
from app.sentiment.Sentiment import roberta_polarity_score
from app.emotions.EmoVideoDict import get_keywords
from app.emotions.api_keys import my_api_key

video_bp = Blueprint('video', __name__)
CORS(video_bp, resources={r"/*": {"origins": { "https://vitalizemind-nodeapi.onrender.com/content/video" } }})

@video_bp.route('/getVideos', methods = ['POST'])
def search_videos():
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

    videosToShow = []

    try:
        next_page_token = ""
        filter_str = keywords_str

        while (len(videosToShow) < 6):

            search_response = youtube.search().list(
                part = 'snippet',
                q = filter_str,
                maxResults = 10,
                safeSearch = 'strict',
                type = 'video',
                videoDefinition = 'high',
                videoDuration = 'medium',
                pageToken = next_page_token
            ).execute()

            if 'items' in search_response:
                for item in search_response['items']:
                    video_id = item['id']['videoId']
                    video_title = item['snippet']['title']
                    comments = video_comments(video_id)
                    comment_score = roberta_polarity_score(comments)
                    try:
                        titleLang = detect(video_title)
                        if titleLang == 'en':
                            if len(videosToShow) == 4 and filter_str != preferences_str:
                                filter_str = preferences_str
                                next_page_token = ""
                                break
                            if len(videosToShow) < 6:
                                if comment_score['neg'] < comment_score['pos']:
                                    videosToShow.append(video_id)
                                    print("passed: " + video_id)
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

    for video in videosToShow:
        print(video)

    return jsonify({ 'videoIds' : videosToShow }), 200


def get_like_dislike(video_id):

    youtube = build('youtube', 'v3', developerKey = my_api_key)

    stat_response = youtube.videos().list(
        part = 'statistics',
        id = video_id
    ).execute()

    try: 
        if 'items' in stat_response:
            stat = stat_response['items'][0]['statistics']
            views = stat['viewCount']
            likes = stat['likeCount']
            ratio = int(likes) / int(views)
            # print("Like to Views ratio: " + str(ratio))
            return ratio
        else: 
            print("stat_response is empty")
    except Exception as e:
        print(e)

def video_comments(video_id):

    youtube = build('youtube', 'v3', developerKey = my_api_key)
    comments = ""

    try:
        comment_response = youtube.commentThreads().list(
            part = 'snippet',
            maxResults = 20,
            videoId = video_id
        ).execute()

        if comment_response:
            for item in comment_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
                try: 
                    language = detect(comment)
                    if language == 'en':
                        if len(comments) > 0:
                            comments += " "
                        comments += comment
                except:
                    pass

    except HttpError as e:
        error_details = e.error_details[0]
        if 'reason' in error_details and error_details['reason'] == 'commentsDisabled':
            print("comments are disabled")
            pass
        else:
            pass

    return comments