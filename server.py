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

# A simple object to hold the global state flag, making it more robust
class AppState:
    initial_data_ready = False

app_state = AppState()

# Background task for updating the cached data
def updateFlightData():
    """
    Function to be run in the background. It fetches new flight data
    and saves it to a JSON file.
    """
    app.logger.info("Starting background data refresh...")
    try:
        flight_data = getFlightRadar(deploy_mode)
        with open(DATA_CACHE_PATH, 'w') as file:
            json.dump(flight_data, file)
        app.logger.info("Background data refresh complete. Data saved to data.json")
        # Update the state flag on success
        app_state.initial_data_ready = True
    except Exception as e:
        app.logger.error(f"Error during data update: {e}")

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

    try:
        # Attempt to read the cached data from the JSON file
        with open(DATA_CACHE_PATH, 'r') as file:
            flight_data = json.load(file)
        return jsonify(flight_data)
    except FileNotFoundError:
        # If the file is not found, it means the cache is not ready.
        # This is where we initiate the background data fetch.
        app.logger.warning("Data file not found. Starting background refresh and waiting.")
        
        # Start the background thread to fetch data, if it's not already running.
        # This is a one-time trigger for the current worker.
        if not app_state.initial_data_ready:
             background_thread = threading.Thread(target=updateFlightData, daemon=True)
             background_thread.start()

        # Wait for the initial data to be ready, with a timeout
        timeout_start = time.time()
        while not app_state.initial_data_ready and (time.time() - timeout_start) < 60:
            app.logger.warning("...")
            time.sleep(1) # Wait a sec

        # Try to read the file again after the wait
        try:
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
    # The Flask application will run and handle requests.
    # The background thread is now started only when the first request comes in and the cache is empty.
    app.run(debug=True)
