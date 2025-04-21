from flask import Flask, request, jsonify, render_template
import os, json, requests

app = Flask(__name__)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)
used_ips = set()

BOT_TOKEN = "7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA"
CHAT_ID = None  # Will be filled dynamically

def send_telegram_message(text):
    global CHAT_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # First time, fetch the chat ID if not set
    if CHAT_ID is None:
        updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()
        try:
            CHAT_ID = updates["result"][-1]["message"]["chat"]["id"]
        except:
            print("Unable to get chat ID. Send a message to your bot first.")
            return

    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.json
    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    if not all([data.get(k) for k in ["fullname", "phone", "towncity", "age", "telegram", "latitude", "longitude"]]):
        return jsonify({"error": "All fields required."}), 400

    if ip in used_ips:
        return jsonify({"error": "This device/IP has already used the form."}), 403

    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return jsonify({"error": "This Telegram username has already used the form."}), 403

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    used_ips.add(ip)

    # Send to Telegram
    msg = f"""New submission:
Full Name: {data['fullname']}
Phone: {data['phone']}
Town/City: {data['towncity']}
Age: {data['age']}
Telegram: @{username}
Location: https://www.google.com/maps?q={data['latitude']},{data['longitude']}"""
    send_telegram_message(msg)

    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your real group link
