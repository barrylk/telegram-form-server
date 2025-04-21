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
def submit():
    if request.is_json:
        data = request.get_json()
    else:
        return jsonify({"error": "Invalid request format"}), 400

    ip = request.remote_addr
    username = data.get("telegram", "").strip().lstrip('@')

    required_fields = ["fullname", "phone", "towncity", "age", "telegram", "latitude", "longitude"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields including location are required."}), 400

    if ip in used_ips:
        return jsonify({"error": "This device/IP has already used the form."}), 403

    filepath = os.path.join(DATA_DIR, f"{username}.json")
    if os.path.exists(filepath):
        return jsonify({"error": "This Telegram username has already used the form."}), 403

    with open(filepath, "w") as f:
        json.dump({
            "fullname": data["fullname"],
            "phone": data["phone"],
            "towncity": data["towncity"],
            "age": data["age"],
            "telegram": username,
            "ip": ip,
            "latitude": data["latitude"],
            "longitude": data["longitude"]
        }, f, indent=2)

    used_ips.add(ip)
    return jsonify({"link": "https://t.me/+APbxtoSb76hmZWZl"})  # Replace with your actual group link

if __name__ == "__main__":
    app.run(debug=True)
