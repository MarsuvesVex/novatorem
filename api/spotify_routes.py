# api/spotify_routes.py
from flask import Blueprint, Response, render_template, request
from .config import Config
from .utils import SpotifyUtils
import requests
import json
import random
from .spotify import  gradientGen, loadImageB64, getTemplate, get

spotify_bp = Blueprint('spotify', __name__, template_folder='templates')


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

def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(500, 1000)
        # below code generates random cubic-bezier values
        x1 = random.random()
        y1 = random.random()*2
        x2 = random.random()
        y2 = random.random()*2
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: 15s, {}ms; animation-timing-function: ease, cubic-bezier({},{},{},{}); }}".format(
                i, left, anim, x1, y1, x2, y2
            )
        )
        left += 4
    return barCSS


def make_spotify_svg(data, background_color, border_color):
    barCount = 84
    contentBar = "".join(["<div class='bar'></div>" for _ in range(barCount)])
    barCSS = barGen(barCount)

    if not "is_playing" in data:
        #contentBar = "" #Shows/Hides the EQ bar if no song is currently playing
        currentStatus = "Recently played:"
        recentPlays = get(RECENTLY_PLAYING_URL)
        recentPlaysLength = len(recentPlays["items"])
        itemIndex = random.randint(0, recentPlaysLength - 1)
        item = recentPlays["items"][itemIndex]["track"]
    else:
        item = data["item"]
        currentStatus = "Vibing to:"

    if item["album"]["images"] == []:
        image = PLACEHOLDER_IMAGE
        barPalette = gradientGen(PLACEHOLDER_URL, 4)
        songPalette = gradientGen(PLACEHOLDER_URL, 2)
    else:
        image = loadImageB64(item["album"]["images"][1]["url"])
        barPalette = gradientGen(item["album"]["images"][1]["url"], 4)
        songPalette = gradientGen(item["album"]["images"][1]["url"], 2)

    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")
    songURI = item["external_urls"]["spotify"]
    artistURI = item["artists"][0]["external_urls"]["spotify"]

    dataDict = {
        "contentBar": contentBar,
        "barCSS": barCSS,
        "artistName": artistName,
        "songName": songName,
        "songURI": songURI,
        "artistURI": artistURI,
        "image": image,
        "status": currentStatus,
        "background_color": background_color,
        "border_color": border_color,
        "barPalette": barPalette,
        "songPalette": songPalette
    }

    return render_template(getTemplate(), **dataDict)
