# app.py - updated to only include object generation
import os
from flask import Flask, make_response, request
from flask_cors import CORS
import random
import json  # Added to use json.dumps for responses

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Health check
@app.route("/")
def health_check():
    return make_response("Healthy.", 200)

# New route to generate an object
@app.route("/generate-object", methods=["POST"])
def generate_object():
    data = request.json
    object_name = data.get("object_name")
    
    # Example logic to generate object stats
    potential = round(random.uniform(0, 1), 2)
    mass = round(random.uniform(0.1, 10), 2)
    condition = round(random.uniform(0, 1), 2)
    decay = round(random.uniform(0, 1), 2)

    object_data = {
        "name": object_name,
        "potential": potential,
        "mass": mass,
        "condition": condition,
        "decay": decay
    }

    return make_response(json.dumps(object_data), 200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run("0.0.0.0", port=port)
