from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

# Your Telegram Bot Token and Group Link
BOT_TOKEN = '7986825869:AAH_I4ZVqmPQx3MZnrBo79YoSdL1YdJ63UA'
GROUP_LINK = 'https://t.me/+APbxtoSb76hmZWZl'

# Location API Key (replace with your own key)
LOCATION_API_KEY = 'a0a9ff9d9beb4f17a5fdd03f49c05142'

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        # Retrieve data from the form submission
        fullname = data['fullname']
        phone = data['phone']
        towncity = data['towncity']
        age = data['age']
        telegram = data['telegram']
        latitude = data['latitude']
        longitude = data['longitude']

        # You can log this data to a file or a database as needed
        print(f"Received data: {fullname}, {phone}, {towncity}, {age}, {telegram}, {latitude}, {longitude}")

        # Optionally: Using the Location API to get more details about the location based on lat, long
        location_info = get_location_info(latitude, longitude)

        # Sending this detailed information to the Telegram group
        message = f"New form submission:\nName: {fullname}\nPhone: {phone}\nLocation: {towncity}\nAge: {age}\nTelegram: {telegram}\nLatitude: {latitude}\nLongitude: {longitude}\nLocation Info: {location_info}"

        # Send the message to Telegram Group
        send_telegram_message(message)

        # Return the link to redirect to the Telegram group
        return jsonify({"link": GROUP_LINK})

    except Exception as e:
        return jsonify({"error": str(e)})

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": "@DevilsGroup",  # Use your channel/group ID or @username
        "text": message
    }
    response = requests.post(url, data=payload)
    return response.json()

def get_location_info(latitude, longitude):
    """
    Use the Location API to get details about the location based on lat, long.
    This can be used to enrich the user's location details.
    """
    location_url = f"https://api.locationiq.com/v1/reverse.php?key={LOCATION_API_KEY}&lat={latitude}&lon={longitude}&format=json"
    response = requests.get(location_url)

    if response.status_code == 200:
        location_data = response.json()
        # Extracting city, state, and country from the location data
        city = location_data.get('address', {}).get('city', 'Unknown City')
        state = location_data.get('address', {}).get('state', 'Unknown State')
        country = location_data.get('address', {}).get('country', 'Unknown Country')
        return f"City: {city}, State: {state}, Country: {country}"
    else:
        return "Location information not available"

if __name__ == '__main__':
    app.run(debug=True)
