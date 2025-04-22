import os
import json
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Directory to store user data
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Set of used IPs to prevent multiple submissions from the same device
used_ips = set()

# Telegram bot settings
BOT_TOKEN = "7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA"
CHAT_ID = "7984761077"  # Replace with your actual chat ID

# API key for location service
LOCATION_API_KEY = "a0a9ff9d9beb4f17a5fdd03f49c05142"  # Replace with your actual API key

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({"error": "Invalid data format"}), 400

    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    if not all([data.get(k) for k in ["fullname", "phone", "towncity", "age", "telegram"]]):
        return jsonify({"error": "All fields required."}), 400

    if ip in used_ips:
        return jsonify({"error": "This device/IP has already used the form."}), 403

    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return jsonify({"error": "This Telegram username has already used the form."}), 403

    # Get user's location using the location API
    location_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={LOCATION_API_KEY}&ip={ip}"
    location_response = requests.get(location_url).json()
    latitude = location_response.get('latitude', 'Unavailable')
    longitude = location_response.get('longitude', 'Unavailable')

    user_data = {
        "fullname": data["fullname"],
        "phone": data["phone"],
        "towncity": data["towncity"],
        "age": data["age"],
        "telegram": username,
        "latitude": latitude,
        "longitude": longitude,
        "ip": ip
    }

    with open(filepath, "w") as f:
        json.dump(user_data, f, indent=2)

    # Send to Telegram bot
    message = "\n".join([
        f"New Telegram Group Request:",
        f"Name: {user_data['fullname']}",
        f"Phone: {user_data['phone']}",
        f"Town/City: {user_data['towncity']}",
        f"Age: {user_data['age']}",
        f"Telegram: @{user_data['telegram']}",
        f"IP: {ip}",
        f"Location: {user_data['latitude']}, {user_data['longitude']}"
    ])
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message}
        )
    except Exception as e:
        print("Telegram send failed:", e)

    used_ips.add(ip)
    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your real group link

if __name__ == "__main__":
    app.run(debug=True)
