from flask import Flask, jsonify, request, abort
from main import getFlightRadar
import os
import json
import threading
import time

app = Flask(__name__)

# Load the API key so only authenticated device can access the web-service
API_KEY = os.environ.get("FLIGHT_RADAR_API_KEY")

DATA_CACHE = "data.json"


# Background task for updating the cached data
def updateFlightData():
    """
    Function to be run in the background. It fetches new flight data
    and saves it to a JSON file.
    """
    while True:
        app.logger.info("Starting background data refresh...")
        try:
            # Call the main function to get the latest flight data
            deploy_mode = 'web-service'
            flight_data = getFlightRadar(deploy_mode)

            # Cache the data to a JSON file
            with open(DATA_CACHE, 'w') as file:
                json.dump(flight_data, file)
            app.logger.info("Background data refresh complete. Data saved to data.json")
        except Exception as e:
            app.logger.error(f"Error in the background data update: {e}")

        # Wait for 30 minutes before refreshing data
        time.sleep(30*60)

# Flask Endpoint for cached data retrieval
@app.route("/data")
def getData():
    """
    An authenticated endpoint to get flight data for TRMNL Polling. 
    It retrieves cached data from data.json and returns instantly. Requires API auth key
    """
    # Get the API key from the request header
    provided_key = request.headers.get("X-API-KEY")

    # Check if the provided key matches the configured key
    if not provided_key or provided_key != API_KEY:
        # If not authenticated, return a 401 Unauthorized error
        abort(401, description="Unauthorized: Invalid API Key")

    try:
        # Read the cached data from the JSON file
        with open(DATA_CACHE, 'r') as file:
            flight_data = json.load(file)
        return jsonify(flight_data)
    except FileNotFoundError:
        # Case where file has not been created yet
        return jsonify({"error" : "Data not available yet. Please wait for initial refresh."}), 503
    except Exception as e:
        app.logger.error(f"An error occurred while reading the cached data: {e}")
        return jsonify({"error" : "Failed to retrieve cached data"}), 500
    
if __name__ == "__main__":
    # Start the background thread for data polling
    # 'daemon=True' ensures that thread exits when main program exits
    background_thread = threading.Thread(target=updateFlightData, daemon=True)
    background_thread.start()

    # Run the Flask application
    app.run(debug=True)