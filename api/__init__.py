
# api/__init__.py
from flask import Flask
from .spotify_routes import spotify_bp
from .youtube_routes import youtube_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(youtube_bp, url_prefix='/youtube')
    return app
