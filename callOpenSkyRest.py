# This script is used to call the flight data API and process the response.

import requests
from flight import Flight  # Import the Flight class to create flight objects

api_source = "https://opensky-network.org/api/states/all" # Base URL for the OpenSky Network API

def getBoxData(lamin, lomin, lamax, lomax):
    """This function retrieves flight data within a specified bounding box."""
    query_url = f"?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}" # Construct the query parameters
    api_url_with_query = api_source + query_url # Construct the full API URL with the query parameters
    flights = callOpenSkyRest(api_url_with_query) # Call the OpenSky REST API with the constructed URL
    return flights  # Return the list of Flight objects retrieved from the API

def callOpenSkyRest(api_url):
    """This function calls the OpenSky REST API and returns the flight data."""
    response = requests.get(api_url)
    if response.status_code == 200:
        flight_data = response.json()
        flights = processFlightData(flight_data) 
        return flights
    else:
        raise Exception(f"Error fetching data from OpenSky API: {response.status_code}")
    
def processFlightData(flight_data):
    """ This function processes the flight data returned by the OpenSky API."""
    flights = []
    for flight in flight_data['states']:
        # Create a Flight object for each flight in the response
        flight_obj = Flight(
            icao24=flight[0],
            callsign=flight[1],
            origin_country=flight[2],
            time_position=flight[3],
            last_contact=flight[4],
            longitude=flight[5],
            latitude=flight[6],
            baro_altitude=flight[7],
            on_ground=flight[8],
            velocity=flight[9],
            true_track=flight[10],
            vertical_rate=flight[11],
            sensors=flight[12],
            geo_altitude=flight[13],
            squawk=flight[14],
            spi=flight[15],
            position_source=flight[16],
            category=None  # Category is not provided in the OpenSky API response
        )
        flights.append(flight_obj)
    return flights  # Return the list of Flight objects
