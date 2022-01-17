from flask import Flask, render_template, request
from cenoteka.CenotekaCrawler import CenotekaCrawler

app = Flask(__name__)

CACHED_URL = None
CACHED_PROIZVODI = None

@app.route("/", methods=["GET", "POST"])
def home():
    global CACHED_URL, CACHED_PROIZVODI
    proizvodi = []
    url = ""
    if request.method == "POST":
        if CACHED_URL is not None and CACHED_URL == request.form["url"]:
            proizvodi = CACHED_PROIZVODI
            url = CACHED_URL
        else:
            cc = CenotekaCrawler(request.form["url"])
            proizvodi = cc.retrieve()
            CACHED_URL = request.form["url"]
            CACHED_PROIZVODI = proizvodi
            url = CACHED_URL
    return render_template("home.jinja", proizvodi=proizvodi, url=url)