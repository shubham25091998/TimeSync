import streamlit as st
from flask import Flask, request, jsonify
import threading
import time
from datetime import datetime

# Shared sync flags
app_requests = {"cpp": False, "android": False}
lock = threading.Lock()
latest_time = None

# Create Flask app for API
api = Flask(__name__)
@api.route("/sync", methods=["POST"])
def sync():
    global latest_time

    data = request.json
    client_type = data.get("client")

    if client_type not in ["cpp", "android"]:
        return jsonify({"error": "Invalid client type"}), 400

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_time = current_time

    # Optional: update which client last pinged
    with lock:
        app_requests[client_type] = True

    return jsonify({"time": current_time, "client": client_type})

# Thread to run Flask API in background
def run_flask():
    api.run(port=5001)

# Start Flask server in thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Streamlit UI
st.title("⏱️ Time Sync Server")

st.write("### 🔄 Status")
st.write("CPP Client:", app_requests["cpp"])
st.write("Android Client:", app_requests["android"])
st.write("Last Synced Time:", latest_time if latest_time else "Not yet synced")

st.write("Listening on port 5001 at `/sync`")

