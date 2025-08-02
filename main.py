import time
start = time.perf_counter()
# Function imports
from aircraftData import load_aircraft_data
from callOpenSkyRest import getBoxData
from geocodeData import getCoords 
from googleSE import googleSE
from configManager import configManager


# Initialisation
aircraft_models = load_aircraft_data('aircraftDataset.csv')  # Load aircraft data from the CSV file
config = configManager()                                     # Load config singleton

address = {'street': config.get_value("address","street"), 
           'city': config.get_value("address","city"),
           'state': config.get_value("address","state"),
           'country': config.get_value("address","country"),
           'postalcode': config.get_value("address","postalcode")}

verbose = 2 # Set verbosity for debugging {0: no output, 1: basic output, 2: detailed output}

# Data retrieval (API)
if verbose > 0:
    print(f"Retrieving nearest flight data for {address['street']}, {address['city']}, {address['state']}, {address['country']}, {address['postalcode']}...")
def getFlightRadar():
    aircraft_models = load_aircraft_data('aircraftDataset.csv')  # Load aircraft data from the CSV file
    street = "16 Lawrence Rd"
    city = "Brisbane"
    state = "QLD"
    country = "AU"
    postalcode = "4032"
    address = {'street': street, 'city': city, 'state': state, 'country': country, 'postalcode': postalcode}  # Create a dictionary with the address components

    coords = getCoords(address)  # Get the coordinates for the specified address
    flight_info = getBoxData(coords)  # Example coordinates for the bounding box
    flight_callsign = flight_info['callsign']
    flight_icao24 = flight_info['icao24']
    flight_typecode = aircraft_models.get(flight_icao24.strip().lower(), "Unknown")

    # testCallOpenSkyRest()  # Call the function to test the OpenSky REST API
    # print(flight_info)  # Print the flight information retrieved from the OpenSky API
    travel_dict = googleSE(flight_callsign)

# Output
if verbose > 0:
    print("The nearest flight to your location is:")
    print(f"Flight {flight_callsign} is a {flight_typecode} and is currently at latitude {flight_info['latitude']} and longitude {flight_info['longitude']}.")
    print(f"Velocity: {flight_info['velocity']} m/s, Squawk: {flight_info['squawk']}, SPI: {flight_info['spi']}")
    print(f"Origin: {travel_dict['origin']}, Destination: {travel_dict['destination']}")

end = time.perf_counter()
print(f"Runtime: {end - start:.4f} seconds")
