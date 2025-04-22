from flask import Flask, request, jsonify, render_template
import os, json, requests

app = Flask(__name__)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

BOT_TOKEN = "7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA"
CHAT_ID = "7984761077"  # Replace with your Telegram user ID or group chat ID
TELEGRAM_GROUP_LINK = "https://t.me/+APbxtoSb76hmZWZl"

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    if not request.is_json:
        return jsonify({"error": "Invalid data format"}), 400

    data = request.get_json()

    if not all([data.get(k) for k in ["fullname", "phone", "towncity", "age", "telegram"]]):
        return jsonify({"error": "All fields required."}), 400

    username = data.get("telegram", "").strip().lstrip('@')
    ip = request.remote_addr
    latitude = data.get("latitude")
    longitude = data.get("longitude")

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

    # Save data to file
    filepath = os.path.join(DATA_DIR, f"{username or ip}.json")
    with open(filepath, "w") as f:
        json.dump(user_data, f, indent=2)

    # Format Telegram message
    message = "\n".join([
        "New Group Join Request:",
        f"Name: {user_data['fullname']}",
        f"Phone: {user_data['phone']}",
        f"City: {user_data['towncity']}",
        f"Age: {user_data['age']}",
        f"Telegram: @{user_data['telegram']}",
        f"IP: {ip}",
        f"Location: {latitude}, {longitude}"
    ])

    # Send to Telegram
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message}
        )
    except Exception as e:
        print("Telegram send failed:", e)

    return jsonify({"link": TELEGRAM_GROUP_LINK})

if __name__ == "__main__":
    app.run(debug=True)
