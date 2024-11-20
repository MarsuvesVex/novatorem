from flask import Flask
from .spotify_routes import spotify_bp  # Note the dot prefix
from .youtube_routes import youtube_bp  # Note the dot prefix

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(youtube_bp, url_prefix='/youtube')

    return app
