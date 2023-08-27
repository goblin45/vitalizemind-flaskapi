from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import requests
from app.api.video import video_bp
from app.api.music import music_bp
from app.api.books import books_bp
from app.api.processor import processor_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://vitalizemind-nodeapi.onrender.com"}})

# Register blueprints
app.register_blueprint(video_bp, url_prefix='/video')
app.register_blueprint(music_bp, url_prefix='/music')
app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(processor_bp, url_prefix='/processor')

@app.route('/sendSearchData', methods=['POST'])
def custom_api():
    try: 
        data_received = request.json
        if 'newSearch' in data_received and 'lastSearches' in data_received:
            new_search = data_received['newSearch']
            last_searches = data_received['lastSearches']

            server2_data = { 'new_search' : new_search, 'last_searches' : last_searches }
            server2_url = 'https://vitalizemind-flaskapi.onrender.com/processor/processSearchData'

            server2_response = requests.post(server2_url, json=server2_data)

            if (server2_response.status_code == 200):
                server2_res_data = server2_response.json()
                print(server2_res_data['message'], flush=True)
                response = { 'message' : server2_res_data['message'], 'score' : server2_res_data['score'], 'clearSearch' : server2_res_data['clear_search']}
                return jsonify(response), 200

            else:
                return jsonify({'error' : server2_response.status_code}) , 400
        else:
            return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)