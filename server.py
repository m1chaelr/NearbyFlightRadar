from flask import Flask, jsonify
from main import getFlightRadar

app = Flask(__name__)

@app.route("/data")
def get_data():
    try:
        flight_data = getFlightRadar()
        return jsonify(flight_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)