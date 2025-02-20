from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = "fishnetsim_data.json"

# Load data from file
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"messages": []}  # Ensure the file always has a messages list

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Route to get all messages
@app.route("/get_data", methods=["GET"])
def get_data():
    data = load_data()
    response = jsonify(data)
    return response

# Route to add a new message
@app.route("/add_message", methods=["POST"])
def add_message():
    data = load_data()
    new_message = request.json  # Expecting JSON { "ip": "...", "message": "...", "timestamp": "...", "nickname": "..." }
    
    if "messages" not in data:
        data["messages"] = []  # Make sure "messages" exists
    
    data["messages"].append(new_message)  # Append new message
    save_data(data)
    
    return jsonify({"message": "Message saved!", "current_messages": data["messages"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
