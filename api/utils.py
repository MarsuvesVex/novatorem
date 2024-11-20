# api/utils.py
from base64 import b64encode
import requests
from io import BytesIO
from colorthief import ColorThief
import random

class SpotifyUtils:
    @staticmethod
    def get_auth(client_id, client_secret):
        return b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")

    @staticmethod
    def bar_gen(bar_count):
        bar_css = ""
        left = 1
        for i in range(1, bar_count + 1):
            anim = random.randint(500, 1000)
            x1 = random.random()
            y1 = random.random() * 2
            x2 = random.random()
            y2 = random.random() * 2
            bar_css += (
                ".bar:nth-child({})  {{ left: {}px; animation-duration: 15s, {}ms; "
                "animation-timing-function: ease, cubic-bezier({},{},{},{}); }}"
            ).format(i, left, anim, x1, y1, x2, y2)
            left += 4
        return bar_css

    @staticmethod
    def gradient_gen(album_art_url, color_count):
        colortheif = ColorThief(BytesIO(requests.get(album_art_url).content))
        return colortheif.get_palette(color_count)

    @staticmethod
    def load_image_b64(url):
        response = requests.get(url)
        return b64encode(response.content).decode("ascii")
