import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    # Spotify Configuration
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
    SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
    SPOTIFY_REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
    SPOTIFY_RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=10"

    # YouTube Configuration
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3/search"
