from flask import Flask, jsonify, request
from datetime import datetime
import pytz 

app = Flask(__name__)

capital_timezones = {
    "Washington": "America/New_York",
    "Ottawa": "America/Toronto",
    "Mexico City": "America/Mexico_City",
    "Brasília": "America/Sao_Paulo",
    "Buenos Aires": "America/Argentina/Buenos_Aires",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "Rome": "Europe/Rome",
    "Madrid": "Europe/Madrid",
    "Warsaw": "Europe/Warsaw",
    "Athens": "Europe/Athens",
    "Cairo": "Africa/Cairo",
    "Nairobi": "Africa/Nairobi",
    "Pretoria": "Africa/Johannesburg",
    "Abuja": "Africa/Lagos",
    "Addis Ababa": "Africa/Addis_Ababa",
    "Moscow": "Europe/Moscow",
    "New Delhi": "Asia/Kolkata",
    "Beijing": "Asia/Shanghai",
    "Tokyo": "Asia/Tokyo",
    "Seoul": "Asia/Seoul",
    "Bangkok": "Asia/Bangkok",
    "Hanoi": "Asia/Ho_Chi_Minh",
    "Jakarta": "Asia/Jakarta",
    "Manila": "Asia/Manila",
    "Canberra": "Australia/Sydney",
    "Wellington": "Pacific/Auckland",
    "Riyadh": "Asia/Riyadh",
    "Tehran": "Asia/Tehran",
    "Baghdad": "Asia/Baghdad",
    "Kabul": "Asia/Kabul",
    "Islamabad": "Asia/Karachi"
}


API_TOKEN = "supersecrettoken123"

"""Implement a TOKEN so only authorized tokens can work - let unauthorized users know"""
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

"""
You code will take a parameter of a Capital City and return the current local time and the UTC Offset (That is a hint btw) in JSON.
"""


@app.route('/api/time/<capital>', methods=['GET'])
@token_required
def get_time(capital):
    timezone_name = capital_timezones.get(capital)
    # Return an informative message if the city isn't in your database.
    if not timezone_name:
        return jsonify({"error": f"Capital city '{capital}' not found in database."}), 404

    timezone = pytz.timezone(timezone_name)
    now = datetime.now(timezone)
    utc_offset = now.strftime('%z')  
    utc_offset_formatted = f"UTC{'+' if int(utc_offset) >= 0 else ''}{int(utc_offset) // 100}"

    return jsonify({
        "capital": capital,
        "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset_formatted
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)