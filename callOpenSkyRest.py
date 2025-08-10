import requests
from flight import Flight  # Import the Flight class to create flight objects
from openSkyAuth import get_token  # Import the function to get the OpenSky API token
import time
from math import cos, sin, pi, radians, atan2, sqrt

flight_states_url = "https://opensky-network.org/api/states/all" # Base URL for the OpenSky Network API
flight_aircraft_url = "https://opensky-network.org/api/flights/aircraft"

def getBoxData(coords, verbose, deploy_mode):
    """This function retrieves flight data within a specified bounding box."""
    # Create box around coordinates
    lat = coords[0]
    lamin = lat - 0.5
    lamax = lat + 0.5

    lon = coords[1]
    lomin = lon - 0.5
    lomax = lon + 0.5

    #  Construct Query and call OpenSky States API
    query = f"?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    states_api_query = flight_states_url + query
    try:
        flights = callOpenSkyRest(states_api_query, type = "states", verbose = verbose, deploy_mode = deploy_mode)
    except Exception as e:
        raise Exception(f"An error occured whilst calling OpenSky: {e}")

    flights_by_distance = getNearestFlight(coords, flights, verbose)  # Get the nearest flight to the specified coordinates

    if verbose > 1:
        print("The list of box-bounded flights are:")
        for flight in flights_by_distance:
            print(f"Flight Callsign: {flight[0].callsign} with icao24: {flight[0].icao24} a distance {flight[1]} from coords")

    return flights_by_distance

def callOpenSkyRest(api_url, type, verbose, deploy_mode):
    """This function calls the OpenSky REST API and returns the flight data."""
    if verbose > 0:
        print("Calling OpenSky REST API with constructed box-bound query...")
        
    token = get_token(deploy_mode)  # Get the OpenSky API token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching data from OpenSky API: {response.status_code}")
    
    if not response:
        raise Exception(f"No data returned from OpenSky API.")

    if response.status_code == 200:
        flight_data = response.json()

        # Catch None or empty lists
        if type == "states":
            if not flight_data.get("states"): # States endpoint
                raise Exception("OpenSky API returned no 'states' data.")
        elif type == "aircraft":
            if not flight_data: #TODO: Add specific structure check here if you intend on ever using this endpoint
                raise Exception("OpenSky returned no 'aircraft' data.")
                
        # Debugging output
        if verbose > 0:
            print(f"Retrieved {len(flight_data['states'])} flights from OpenSky API.")
        elif verbose > 1:
            print(f"Box-Bounded Flight Data: {flight_data}")
        
        # Process the flight data based on type
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

def getNearestFlight(coords, flights, verbose):
    """This function retrieves the nearest flight to the specified coordinates."""
    # Earth radius (constant) (km)
    earth_R = 6378
    # Home coordinates vector (Polar form)
    coord_x_pos = earth_R * cos(coords[0]) * cos(coords[1])
    coord_y_pos = earth_R * cos(coords[0]) * sin(coords[1])
    coords_vector_pol = (coord_x_pos, coord_y_pos)

    # Home coordinates (radians)
    coords_lat_rad = radians(coords[0])
    coords_lon_rad = radians(coords[1])
    
    # Flight storage
    flights_distance = []

    # Calculate each flight's distance from the origin and return a list of flights sorted on distance (asc)
    for flight in flights:
        if flight.latitude is not None and flight.longitude is not None:
            
            if verbose > 2:
                print(f"Calculating distance of flight: {flight.callsign}, ICAO24: {flight.icao24}, Latitude: {flight.latitude}, Longitude: {flight.longitude}")

            # Euclidean distance (lat/lon)
            euclidean_distance = ((flight.latitude - coords[0]) ** 2 + (flight.longitude - coords[1]) ** 2) ** 0.5
            
            # Polar distance (km)
            flight_x_pos = earth_R * cos(flight.latitude) * cos(flight.longitude)
            flight_y_pos = earth_R * cos(flight.latitude) * sin(flight.longitude)
            flight_vector = (flight_x_pos, flight_y_pos)
            polar_distance = ((coords_vector_pol[0] - flight_vector[0]) ** 2 + (coords_vector_pol[1] - flight_vector[1]) ** 2) ** 0.5

            # Haversine formula method
            flight_lat_rad = radians(flight.latitude)
            flight_lon_rad = radians(flight.longitude)

            delta_lat = coords_lat_rad - flight_lat_rad
            delta_lon = coords_lon_rad - flight_lon_rad

            a = sin(delta_lat / 2) ** 2 + cos(flight_lat_rad) * cos(coords_lat_rad) * sin(delta_lon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            haversine_distance = earth_R * c
            

            # Store Flight and distance to origin
            flights_distance.append((flight, haversine_distance))

    # Sort the box-bounded flights in order of distance (ascending)
    flights_distance.sort(key=lambda x: x[1])
    return flights_distance