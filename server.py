from flask import Flask, jsonify, request, abort
import os
import json

app = Flask(__name__)

# Load the API key from environment variables for security
API_KEY = os.environ.get("FLIGHT_RADAR_API_KEY")
DATA_CACHE_PATH = "data.json"

@app.route("/data")
def getData():
    """
    TRMNL polling endpoint. It retrieves cached data from the
    local JSON file and returns it instantly.
    Requires API Key authentication.
    """
    provided_key = request.headers.get("X-API-KEY")

    if not provided_key or provided_key != API_KEY:
        abort(401, description="Unauthorized: Invalid API Key")

    try:
        with open(DATA_CACHE_PATH, 'r') as file:
            flight_data = json.load(file)
        return jsonify(flight_data)
    except FileNotFoundError:
        # This will happen on the very first poll after deployment.
        app.logger.error("Data cache file not found.")
        return jsonify({"error": "Data not yet available. Please wait for the first GitHub Action run."}), 503
    except Exception as e:
        app.logger.error(f"An error occurred while reading the cached data: {e}")
        return jsonify({"error": "Failed to retrieve cached data"}), 500

@app.route("/upload", methods=["POST"])
def upload_data():
    """
    Endpoint for GitHub Actions to POST fresh flight data.
    Requires API Key authentication.
    """
    provided_key = request.headers.get("X-API-KEY")

    if not provided_key or provided_key != API_KEY:
        abort(401, description="Unauthorized: Invalid API Key")

    try:
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "Invalid JSON data received"}), 400

        with open(DATA_CACHE_PATH, "w") as file:
            json.dump(new_data, file)
        
        app.logger.info("Data updated successfully via POST request.")
        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        app.logger.error(f"Failed to save data: {e}")
        return jsonify({"error": f"Failed to save data: {e}"}), 500

if __name__ == "__main__":
    # The application will run without a background thread.
    app.run(debug=True)
