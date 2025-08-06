# Function imports
from aircraftData import load_aircraft_data
from callOpenSkyRest import getBoxData
from geocodeData import getCoords 
from googleSE import googleSE
import os
from configManager import configManager
from datetime import datetime
from zoneinfo import ZoneInfo

def getFlightRadar(deploy_mode):
    # Initialisation
    aircraft_models = load_aircraft_data('aircraftDetailDataset.csv')  # Load aircraft data from the CSV file

    # Read the specified deploy mode and load environment variables respectively
    match deploy_mode:
        case 'web-service':
            address = {'street': os.environ.get('STREET'), 
                'city': os.environ.get('CITY'),
                'state': os.environ.get('STATE'),
                'country': os.environ.get('COUNTRY'),
                'postalcode': os.environ.get('POSTALCODE')}
        case 'local-host':
            config = configManager() # Load config singleton
            address = {'street': config.get_value("address","street"), 
                'city': config.get_value("address","city"),
                'state': config.get_value("address","state"),
                'country': config.get_value("address","country"),
                'postalcode': config.get_value("address","postalcode")}
            
    verbose = 1 # Set verbosity for debugging {0: no output, 1: basic output, 2: detailed output}

    # Data retrieval (API)
    if verbose > 0:
        print(f"Retrieving nearest flight data for {address['street']}, {address['city']}, {address['state']}, {address['country']}, {address['postalcode']}...")

    coords = getCoords(address, deploy_mode)                # Geocoding
    flights_distance = getBoxData(coords, verbose, deploy_mode)  # Retrieve flight data within the bounding box

    # Loop through the list of returned flights and return the closest flight with a valid typecode
    flight_typecode = "Unknown"
    i = 0
    while flight_typecode == "Unknown":
        flight_record = flights_distance[i]
        flight_typecode = aircraft_models.get(flight_record[0].icao24.strip().lower(), "Unknown")
        print(f"The flight: {flight_record[0].icao24} is a type: {flight_typecode}")
        i += 1
    

    # Data processing
    flight_info = flight_record[0]
    flight_callsign = flight_info.callsign.strip()
    flight_distance = flight_record[1]
    flight_lat = flight_info.latitude
    flight_lon = flight_info.longitude
    flight_vel = flight_info.velocity
    flight_squawk = flight_info.squawk
    flight_spi = flight_info.spi

    if verbose > 1:
        print(f"The nearest flight is {flight_callsign}, which is a {flight_typecode} and is {flight_distance} from {coords}")

    # Data retrieval (Google PSE)
    travel_dict = googleSE(flight_callsign, verbose, deploy_mode)

    # Output
    if verbose > 1:
        print("The nearest flight to your location is:")
        print(f"Flight {flight_callsign} is a {flight_typecode} and is currently at latitude {flight_lat} and longitude {flight_lon}.")
        print(f"Which is at a distance of: {flight_distance} from the origin")
        print(f"Velocity: {flight_vel} m/s, Squawk: {flight_squawk}, SPI: {flight_spi}")
        print(f"Origin: {travel_dict['origin']}, Destination: {travel_dict['destination']}")
    
    # Store the current time in Brisbane
    timezone = ZoneInfo(f"Australia/{address['city']}")
    now = datetime.now(timezone)
    current_time = now.strftime("%H:%M %d %B %Y")

    # Store dictionary output
    output = {'callsign' : flight_callsign,
              'typecode' : flight_typecode,
              'origin' : travel_dict['origin'],
              'destination' : travel_dict['destination'],
              'velocity' : flight_vel,
              'distance' : flight_distance,
              'updated_at' : current_time
            }

    return output