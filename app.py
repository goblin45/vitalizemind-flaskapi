from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import requests

app = Flask(__name__)
CORS(app, resources={r"/sendSearchData": {"origins": "http://localhost:3500"}})

@app.route('/sendSearchData', methods=['POST'])
def custom_api():
    try: 
        data_received = request.json
        if 'newSearch' in data_received and 'lastSearches' in data_received:
            new_search = data_received['newSearch']
            last_searches = data_received['lastSearches']

            server2_data = { 'new_search' : new_search, 'last_searches' : last_searches }
            server2_url = 'http://127.0.0.1:5001/processSearchData'

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
    app.run(debug = True, port = 5000)