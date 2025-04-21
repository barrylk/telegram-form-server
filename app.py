from flask import Flask, request, jsonify, render_template
import os
import json
from datetime import datetime

app = Flask(_name_)

# Replace with your actual group link
TELEGRAM_LINK = "https://t.me/+APbxtoSb76hmZWZl"

# Storage folder
STORAGE_FOLDER = "submissions"
if not os.path.exists(STORAGE_FOLDER):
    os.makedirs(STORAGE_FOLDER)

# Track used IPs/devices
used_ips = set()
used_devices = set()

@app.route("/")
def form_page():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.get_json()

    required_fields = ["fullname", "phone", "towncity", "age", "telegram"]
    if not all(field in data and data[field].strip() for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    ip = request.remote_addr
    device_id = request.headers.get("User-Agent", "")

    if ip in used_ips or device_id in used_devices:
        return jsonify({"error": "Access denied. You have already submitted."}), 403

    username = data["telegram"].lstrip("@")
    user_folder = os.path.join(STORAGE_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    filename = os.path.join(user_folder, "data.json")
    with open(filename, "w") as f:
        json.dump({
            "fullname": data["fullname"],
            "phone": data["phone"],
            "towncity": data["towncity"],
            "age": data["age"],
            "telegram": data["telegram"],
            "ip": ip,
            "device": device_id,
            "timestamp": datetime.utcnow().isoformat()
        }, f, indent=2)

    # Mark IP and device as used
    used_ips.add(ip)
    used_devices.add(device_id)

    return jsonify({"link": TELEGRAM_LINK})
