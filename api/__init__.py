# api/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import blueprints after Flask app initialization to avoid circular imports
    from .spotify_routes import spotify_bp
    from .youtube_routes import youtube_bp

    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(youtube_bp, url_prefix='/youtube')

    return app
