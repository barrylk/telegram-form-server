from flask import Flask, request, jsonify
import os, json

app = Flask(_name_)
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)
used_ips = set()

@app.route("/submit", methods=["POST"])
def handle_form():
    data = request.json
    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    if not all([data.get(k) for k in ["fullname", "phone", "towncity", "age", "telegram"]]):
        return jsonify({"error": "All fields required."}), 400

    if ip in used_ips:
        return jsonify({"error": "This device/IP has already used the form."}), 403

    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return jsonify({"error": "This Telegram username has already used the form."}), 403

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    used_ips.add(ip)
    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your real link