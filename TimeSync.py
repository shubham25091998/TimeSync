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
    global app_requests, latest_time

    data = request.json
    client_type = data.get("client")

    if client_type not in app_requests:
        return jsonify({"error": "Invalid client type"}), 400

    with lock:
        app_requests[client_type] = True
        
        if (app_requests[client_type]):
        	current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            latest_time = current_time
            # Reset for next round
            #app_requests = {"cpp": False, "android": False}
            return jsonify({"time": current_time})
        else:
        	return jsonify({"message": f"Waiting for the other client"})


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

