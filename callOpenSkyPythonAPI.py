from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import time
import json


# Read the OpenSky credentials from a JSON file
with open('API/credentials.json') as file:
    credentials = json.load(file)

open_sky_user = credentials['openSkyUsername']
open_sky_pwd = credentials['openSkyPassword']

# Start the OpenSky API client
api = OpenSkyApi(open_sky_user, open_sky_pwd)

def getNearestFlight(user_coords, aircraft_models):
    """
    This function retrieves the nearest flight to the user's location.
    :param user_lat: User's latitude
    :param user_lon: User's longitude
    :param aircraft_models: Aircraft models dictionary
    :return: Nearest flight object or None if no flights are found
    """
    user_lat, user_lon = user_coords  # Unpack the user's coordinates
    flight_info = {}  # Initialize an empty dictionary to store flight information
    bbox = (user_lat - 0.5, user_lat + 0.5, user_lon - 0.5, user_lon + 0.5)  # Bounding box around the user's location

    nearest_flight = None
    nearest_flight_distance = float('inf')  # Initialize with a large number
    # Get the current time in UNIX timestamp format
    current_time = int(time.time())
    state_vectors = api.get_states()

    for state in state_vectors.states:
        # Exclude flights without a known typecode
        typecode = aircaft_models.get(state.icao24,strip().lower(), "Unknown")
        if typecode == "Unknown":
            continue

        # Calculate the distance to the user's location
        state_pos_vector = (state.longitude, state.latitude) # Position vector of the flight
        user_pos_vector = (user_lon, user_lat) # User's position vector (origin)

        distance = ((state_pos_vector[0] - user_pos_vector[0]) ** 2 + (state_pos_vector[1] - user_pos_vector[1]) ** 2) ** 0.5 # Calculate distance

        if nearest_flight is None or distance < nearest_flight_distance:
            nearest_flight = state
            nearest_flight_distance = distance
    
    if nearest_flight is not None:
        typecode = aircraft_models.get(nearest_flight.icao24.strip().lower(), "Unknown")
        
        # Get 1 hour ago in UNIX timestamp
        hour_ago = current_time - 3600  # One hour ago in UNIX timestamp

        # Call flights within the last hour
        flights = api.get_flights(nearest_flight.icao24, hour_ago, current_time)

        if flights:
            flight = flights[0]  # Get the first flight in the list
            flight_info = {
                'icao24': flight.icao24,
                typecode: aircraft_models.get(flight.icao24.strip().lower(), "Unknown"),
                'origin': flight.estDepartureAirport,
                'destination': flight.estArrivalAirport,
                'velocity': flight.velocity,
                'longitude': flight.longitude,
                'latitude': flight.latitude,
                'baro_altitude': flight.baroAltitude,
            }
    return flight_info