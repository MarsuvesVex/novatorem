
# api/spotify_routes.py
from flask import Blueprint, Response, render_template, request
from .config import Config
from .utils import SpotifyUtils
import requests
import json
import random

""" spotify_bp = Blueprint('spotify', __name__, template_folder='templates') """
spotify_bp = Blueprint('spotify', __name__)

class SpotifyAPI:
    def __init__(self):
        self.token = ""
        self.config = Config()

    def refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.config.SPOTIFY_REFRESH_TOKEN,
        }
        headers = {"Authorization": f"Basic {SpotifyUtils.get_auth(self.config.SPOTIFY_CLIENT_ID, self.config.SPOTIFY_SECRET_ID)}"}
        response = requests.post(self.config.SPOTIFY_REFRESH_TOKEN_URL, data=data, headers=headers).json()

        try:
            return response["access_token"]
        except KeyError:
            print(json.dumps(response))
            raise KeyError(str(response))

    def get(self, url):
        if not self.token:
            self.token = self.refresh_token()

        response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})

        if response.status_code == 401:
            self.token = self.refresh_token()
            response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"})
            return response.json()
        elif response.status_code == 204:
            raise Exception(f"{url} returned no data.")

        return response.json()

spotify_api = SpotifyAPI()

@spotify_bp.route("/", defaults={"path": ""})
@spotify_bp.route("/<path:path>")
def spotify_card(path):
    background_color = request.args.get('background_color') or "181414"
    border_color = request.args.get('border_color') or "181414"

    try:
        data = spotify_api.get(Config.SPOTIFY_NOW_PLAYING_URL)
    except Exception:
        data = spotify_api.get(Config.SPOTIFY_RECENTLY_PLAYING_URL)

    svg = make_spotify_svg(data, background_color, border_color)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp

def make_spotify_svg(data, background_color, border_color):
    bar_count = 84
    content_bar = "".join(["<div class='bar'></div>" for _ in range(bar_count)])
    bar_css = SpotifyUtils.bar_gen(bar_count)

    if not "is_playing" in data:
        current_status = "Recently played:"
        recent_plays = spotify_api.get(Config.SPOTIFY_RECENTLY_PLAYING_URL)
        recent_plays_length = len(recent_plays["items"])
        item_index = random.randint(0, recent_plays_length - 1)
        item = recent_plays["items"][item_index]["track"]
    else:
        item = data["item"]
        current_status = "Vibing to:"

    if not item["album"]["images"]:
        raise ValueError("No album art available")

    image = SpotifyUtils.load_image_b64(item["album"]["images"][1]["url"])
    bar_palette = SpotifyUtils.gradient_gen(item["album"]["images"][1]["url"], 4)
    song_palette = SpotifyUtils.gradient_gen(item["album"]["images"][1]["url"], 2)

    artist_name = item["artists"][0]["name"].replace("&", "&amp;")
    song_name = item["name"].replace("&", "&amp;")
    song_uri = item["external_urls"]["spotify"]
    artist_uri = item["artists"][0]["external_urls"]["spotify"]

    data_dict = {
        "content_bar": content_bar,
        "bar_css": bar_css,
        "artist_name": artist_name,
        "song_name": song_name,
        "song_uri": song_uri,
        "artist_uri": artist_uri,
        "image": image,
        "status": current_status,
        "background_color": background_color,
        "border_color": border_color,
        "bar_palette": bar_palette,
        "song_palette": song_palette
    }

    return render_template('spotify.html.j2', **data_dict)
