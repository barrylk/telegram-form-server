from flask import Flask, request, jsonify, render_template
import os, json

app = Flask(__name__)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)
used_ips = set()

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.get_json()
    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    required_fields = ["fullname", "phone", "towncity", "age", "telegram", "location"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required, including location."}), 400

    if ip in used_ips:
        return jsonify({"error": "This device/IP has already used the form."}), 403

    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return jsonify({"error": "This Telegram username has already used the form."}), 403

    with open(filepath, "w") as f:
        json.dump({
            "Full Name": data["fullname"],
            "Phone Number": data["phone"],
            "Town/City": data["towncity"],
            "Age": data["age"],
            "Telegram": username,
            "IP Address": ip,
            "Location": data["location"]
        }, f, indent=2)

    used_ips.add(ip)
    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your actual Telegram group link

if _name_ == "_main_":
    app.run(debug=True)
