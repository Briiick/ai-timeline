from flask import Flask, jsonify
from datetime import date
import logging
import requests
import os
from firebase_admin import credentials, initialize_app
from firebase_functions import https_fn
from flask_cors import CORS

# Initialize Firebase app
cred = credentials.Certificate('firebase-admin.json')
firebase_app = initialize_app(cred)

# Create a custom logger
logger = logging.getLogger(__name__)

# Set level of logger
logger.setLevel(logging.ERROR)

# Create handlers
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(handler)

# Get the Google Apps Script API URL from the environment variable
gas_api_url = os.environ.get('GAS_API_URL')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the AI Timeline API!"

@app.route('/api/createsummary')
def create_summary():
    try:
        # Make a request to the Google Apps Script API to fetch the data
        response = requests.get(f'{gas_api_url}?action=createSummary')
        data = response.json()
        return jsonify(data)
    except requests.exceptions.JSONDecodeError as e:
        # Handle JSON decoding error
        error_message = f"Failed to decode JSON response: {str(e)}"
        logger.error(error_message)
        return jsonify({"error": error_message}), 500
    except Exception as e:
        # Handle other exceptions
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        return jsonify({"error": error_message}), 500

@app.route('/api/summaries/all')
def get_all_summaries():
    try:
        # Make a request to the Google Apps Script API to fetch all summaries
        print("f'launching request: {gas_api_url}?action=getAllSummaries'")
        response = requests.get(f'{gas_api_url}?action=getAllSummaries')

        # Check the response status code
        if response.status_code == 200:
            print("success")
            print(response.content)
            # Directly return the response content as JSON
            return response.content, 200, {'Content-Type': 'application/json'}
        else:
            # Handle non-200 status codes
            error_message = f"API request failed with status code: {response.status_code}"
            logger.error(error_message)
            return jsonify({"error": error_message}), response.status_code

    except Exception as e:
        # Handle other exceptions
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        return jsonify({"error": error_message}), 500

@https_fn.on_request(max_instances=1)
def ai_timelines(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
