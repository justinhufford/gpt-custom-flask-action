# app.py - this is the main Heroku app that runs all of the Actions
from flask import Flask, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
import requests
import re
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Health check
@app.route("/")
def health_check():
    return make_response("Healthy.", 200)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_RED_URL', 'sqlite:///golfcommand.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    strength = db.Column(db.Float, default=0.8)
    accuracy = db.Column(db.Float, default=0.8)
    swing_power = db.Column(db.Float, default=1.0)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    qty = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(200), nullable=True)
    potential = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Float, nullable=False)
    decay = db.Column(db.Float, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)


# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    upgrade()

# Health check
@app.route("/")
def health_check():
    return make_response("Healthy.", 200)

# This is not included in the blog for simplicity's sake, but cleans up
# the content a bit before sending it back to the GPT.
def remove_html_tags_and_whitespace(html):
    content = re.sub(r"\<.*?\>|[\t\n]", "", html)
    return content

# Fetches HTML from any given url. Expects the url to be a query parameter.
@app.route("/fetch-html", methods=["GET"])
def fetch_html():
    url = request.args.get("url")
    page = requests.get(url)
    html_text = page.text
    encoded_html = html_text.encode(page.encoding)
    decoded_html = encoded_html.decode(page.encoding)
    html_content = remove_html_tags_and_whitespace(decoded_html)

    return make_response({"html": html_content}, 200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run("0.0.0.0", port=port)
