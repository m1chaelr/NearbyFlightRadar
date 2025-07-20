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

coords = getCoords(address)                # Geocoding
flight_info = getBoxData(coords, verbose)  # Retrieve flight data within the bounding box

# Data processing
flight_callsign = flight_info['callsign'].strip()
flight_icao24 = flight_info['icao24']
flight_typecode = aircraft_models.get(flight_icao24.strip().lower(), "Unknown") # Lookup aircraft model by ICAO24 code

if verbose > 1:
    print(f"The nearest flight is {flight_callsign}, which is a {flight_typecode}")

# Data retrieval (Google PSE)
travel_dict = googleSE(flight_callsign, verbose)

# Output
if verbose > 0:
    print("The nearest flight to your location is:")
    print(f"Flight {flight_callsign} is a {flight_typecode} and is currently at latitude {flight_info['latitude']} and longitude {flight_info['longitude']}.")
    print(f"Velocity: {flight_info['velocity']} m/s, Squawk: {flight_info['squawk']}, SPI: {flight_info['spi']}")
    print(f"Origin: {travel_dict['origin']}, Destination: {travel_dict['destination']}")

end = time.perf_counter()
print(f"Runtime: {end - start:.4f} seconds")
