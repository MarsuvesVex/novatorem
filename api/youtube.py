
# api/youtube_routes.py
from flask import Blueprint, jsonify
from api.config import Config
import requests
from dotenv import load_dotenv, find_dotenv
import os

youtube_bp = Blueprint('youtube', __name__)

# Load environment variables
load_dotenv(find_dotenv())
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Flask app
app = Flask(__name__)

@app.route('/recent-videos/<channel_id>', methods=['GET'])
def get_recent_videos(channel_id):
    """
    Fetch the 5 most recent videos from a YouTube channel.
    :param channel_id: YouTube channel ID
    :return: JSON response with video details
    """
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 5
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from YouTube API"}), response.status_code

    data = response.json()

    videos = [
        {
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "publishedAt": item["snippet"]["publishedAt"]
        }
        for item in data.get("items", [])
        if item["id"].get("videoId")  # Ensure it's a video
    ]

    return jsonify({"videos": videos})

if __name__ == '__main__':
    app.run(debug=True)
