from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import time


# Read the OpenSky credentials from a JSON file
with open('API/credentials.json') as file:
    credentials = json.load(file)
open_sky_user = credentials['openSkyUsername']
open_sky_pwd = credentials['openSkyPassword']

# Start the OpenSky API client
api = OpenSkyApi(openSkyUsername, openSkyPassword)

def getNearestFlight(user_lat, user_lon, aircraft_models):
    """
    This function retrieves the nearest flight to the user's location.
    :param user_lat: User's latitude
    :param user_lon: User's longitude
    :param aircraft_models: Aircraft models dictionary
    :return: Nearest flight object or None if no flights are found
    """

    bbox = (user_lat - 0.5, user_lon - 0.5, user_lat + 0.5, user_lon + 0.5)  # Bounding box around the user's location

    nearest_flight = None
    state_vectors = api.get_states(self, 0, None, bbox)

    for state in state_vectors:
        # Exclude flights without a known typecode
        
    