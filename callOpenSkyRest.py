# This script is used to call the flight data API and process the response.

import requests
from flight import Flight  # Import the Flight class to create flight objects
from opensky_auth import get_token  # Import the function to get the OpenSky API token
import time

flight_states_url = "https://opensky-network.org/api/states/all" # Base URL for the OpenSky Network API
flight_aircraft_url = "https://opensky-network.org/api/flights/aircraft"

temp_url = "https://opensky-network.org/api/flights/all?begin=1517227200&end=1517230800"

def testCallOpenSkyRest():
    result = callOpenSkyRest(temp_url, type = "aircraft")
    print(result)  # Print the number of flights retrieved from the API

def getBoxData(coords):
    """This function retrieves flight data within a specified bounding box."""
    lat = coords[0]
    lamin = lat - 0.5
    lamax = lat + 0.5

    lon = coords[1]
    lomin = lon - 0.5
    lomax = lon + 0.5

    query = f"?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}" # Construct the query parameters
    states_query = flight_states_url + query # Construct the full API URL with the query parameters
    flights = callOpenSkyRest(states_query, type = "states") # Call the OpenSky REST API with the constructed URL

    nearest_flight, distance = getNearestFlight(coords, flights)  # Get the nearest flight to the specified coordinates

    flight_info = None  # Initialize flight_info to None

    if nearest_flight:
        icao24 = nearest_flight.icao24.strip().lower()
        now = int(time.time())
        half_ago = now - 1800 # 30 minutes ago

        one_day_ago = now - 86400          # 24 hours ago
        one_day_one_hour_ago = now - 90000 # 25 hours ago

        query = f"?icao24={icao24}&begin={one_day_one_hour_ago}&end={one_day_ago}"
        aircraft_query = flight_aircraft_url + query  # Construct the API URL for aircraft data
        result = callOpenSkyRest(aircraft_query, type = "aircraft") 

        flight_info = {
            "icao24": nearest_flight.icao24,
            "latitude": nearest_flight.latitude,
            "longitude": nearest_flight.longitude,
            "velocity": nearest_flight.velocity,
            "depAirport": nearest_flight.estDepartureAirport,
            "arrAirport": nearest_flight.estArrivalAirport,
        }
    return flight_info  # Return the list of Flight objects retrieved from the API

def callOpenSkyRest(api_url, type):
    """This function calls the OpenSky REST API and returns the flight data."""
    token = get_token()  # Get the OpenSky API token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        flight_data = response.json()
        print(flight_data)

        if type == "states":
            result = processStatesData(flight_data) 
        elif type == "aircraft":
            result = processAircraftData(flight_data)
        else:
            raise ValueError("Invalid type specified. Use 'states' or 'aircraft'.")
        return result
    
    else:
        raise Exception(f"Error fetching data from OpenSky API: {response.status_code}")
    
def processAircraftData(flight_data):
    """ This function processes the flight data returned by the OpenSky Aircraft API."""
    flights = []
    for flight in flight_data['states']:
        # Create a Flight object for each flight in the response
        flight_obj = Flight(
            icao24=flight[0],
            firstseen=flight[1],
            estDepartureAirport=flight[2], # use ourariports.com
            lastSeen=flight[3],
            estArrivalAirport=flight[4],
            callsign=flight[5],
            estDepartureAirportHorizDistance=flight[6],
            estDepartureAirportVertDistance=flight[7],
            estArrivalAirportHorizDistance=flight[8],
            estArrivalAirportVertDistance=flight[9],
            departureAirportCandidatesCount=flight[10],
            arrivalAirportCandidatesCount=flight[11]
        )
        flights.append(flight_obj)

    for flight in flights:
        if flight.estDepartureAirport is not None and flight.estArrivalAirport is not None:
            return flight
        else:
            print(f"Flight {flight.icao24} does not have a valid departure or arrival airport. Checking next flight.")

def processStatesData(flight_data):
    """ This function processes the flight data returned by the OpenSky States API."""
    flights = []
    for flight in flight_data['states']:
        # Create a Flight object 
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

def getNearestFlight(coords, flights):
    """This function retrieves the nearest flight to the specified coordinates."""
    nearest_flight = None
    min_distance = float('inf') # Initialize minimum distance to infinity

    for flight in flights:
        if flight.latitude is not None and flight.longitude is not None:
            # Calculate the Flight's Euclidean distance from the origin (home)
            distance = ((flight.latitude - coords[0]) ** 2 + (flight.longitude - coords[1]) ** 2) ** 0.5
            
            # Store the closes flight
            if distance < min_distance:
                min_distance = distance
                nearest_flight = flight
    return nearest_flight, distance  # Return the nearest Flight object