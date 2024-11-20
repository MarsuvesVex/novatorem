from flask import Blueprint, jsonify, render_template, request
from .config import Config  # Note the dot prefix
import requests

youtube_bp = Blueprint('youtube', __name__, template_folder='templates')

@youtube_bp.route('/recent-videos/<channel_id>', methods=['GET'])
def get_recent_videos(channel_id):
    """Fetch and display recent videos from a YouTube channel"""
    background_color = request.args.get('background_color', '#181414')
    border_color = request.args.get('border_color', '#282828')

    params = {
        "key": Config.YOUTUBE_API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 5,
        "type": "video"
    }

    try:
        response = requests.get(Config.YOUTUBE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        videos = [
            {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channelTitle": item["snippet"]["channelTitle"]
            }
            for item in data.get("items", [])
            if item["id"].get("videoId")
        ]

        return render_template(
            'youtube.html.j2',
            videos=videos,
            background_color=background_color,
            border_color=border_color
        )

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data from YouTube API: {str(e)}"}), 500
