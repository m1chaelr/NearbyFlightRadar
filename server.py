from flask import Flask, jsonify, request, abort
from main import getFlightRadar
import os

app = Flask(__name__)

# Load the API key so only authenticated device can access the web-service
API_KEY = os.environ.get("FLIGHT_RADAR_API_KEY")


@app.route("/data")
def get_data():
    """
    An authenticated endpoint to get flight data.
    Requires a valid API key in the 'X-API-KEY' header.
    """
    # Get the API key from the request header
    provided_key = request.headers.get("X-API-KEY")

    # Check if the provided key matches the configured key
    if not provided_key or provided_key != API_KEY:
        # If not authenticated, return a 401 Unauthorized error
        abort(401, description="Unauthorized: Invalid API Key")

    try:
        deploy_mode = 'web-service'
        flight_data = getFlightRadar(deploy_mode)
        return jsonify(flight_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)