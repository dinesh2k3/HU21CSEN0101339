from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
STORE = []

# Function to fetch numbers from third-party API
def fetch_number(number_type):
    try:
        url = f"http://20.244.56.144/test/{number_type}"
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return int(response.text)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    return None

# Endpoint to calculate the average
@app.route('/numbers/<string:number_type>', methods=['GET'])
def get_average(number_type):
    global STORE

    if number_type not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number type"}), 400

    prev_state = STORE.copy()
    number = fetch_number(number_type)

    if number is not None and number not in STORE:
        if len(STORE) >= WINDOW_SIZE:
            STORE.pop(0)  # Remove oldest number
        STORE.append(number)

    if len(STORE) == 0:
        return jsonify({"error": "No numbers to calculate average"}), 500

    avg = sum(STORE) / len(STORE)

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": STORE,
        "numbers": STORE,
        "avg": round(avg, 2)
    })

if __name__ == '__main__':
    app.run(port=9876)
