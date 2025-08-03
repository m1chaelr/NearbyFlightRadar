from flask import Flask, jsonify, request, abort
from main import getFlightRadar
import os
import json
import threading
import time

app = Flask(__name__)

# Load the API key so only authenticated device can access the web-service
API_KEY = os.environ.get("FLIGHT_RADAR_API_KEY")

DATA_CACHE_PATH = "data.json"
deploy_mode = 'web-service'


# Background task for updating the cached data
def updateFlightData():
    """
    Function to be run in the background. It fetches new flight data
    and saves it to a JSON file.
    """
    global initial_data_ready

    # Run the first data fetch immediately on startup
    app.logger.info("Starting initial background data refresh...")
    try:
        flight_data = getFlightRadar(deploy_mode)
        with open(DATA_CACHE_PATH, 'w') as file:
            json.dump(flight_data, file)
        app.logger.info("Initial background data refresh complete. Data saved to data.json")
        initial_data_ready = True
    except Exception as e:
        app.logger.error(f"Error during initial data update: {e}")

    # Then enter loop for subsequent updates
    while True:
        time.sleep(30 * 60)
        app.logger.info("Starting periodic background data refresh...")
        try:
            # Call the main function to get the latest flight data
            flight_data = getFlightRadar(deploy_mode)

            # Cache the data to a JSON file
            with open(DATA_CACHE_PATH, 'w') as file:
                json.dump(flight_data, file)
            app.logger.info("Periodic background data refresh complete. Data saved to data.json")
        except Exception as e:
            app.logger.error(f"Error in the background data update: {e}")

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

    # Wait for the initial data to be ready, with a timeout
    timeout_start = time.time()
    app.logger.warning("Data file not found. Waiting until it's set")
    while not initial_data_ready and (time.time() - timeout_start) < 60:
        app.logger.warning("...")
        time.sleep(1) # Wait a sec

    try:
        # Read the cached data from the JSON file
        with open(DATA_CACHE_PATH, 'r') as file:
            flight_data = json.load(file)
        return jsonify(flight_data)
    except FileNotFoundError:
        # If after waiting, the file still doesn't exist, something is wrong
        app.logger.error("Data file not found after waiting. Background thread likely failed.")
        return jsonify({"error" : "Data not available yet. Background task failed to initialise."}), 503
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