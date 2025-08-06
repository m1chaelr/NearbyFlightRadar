# Function imports
from aircraftData import load_aircraft_data
from callOpenSkyRest import getBoxData
from geocodeData import getCoords 
from googleSE import googleSE
import os
from configManager import configManager
from datetime import datetime
from zoneinfo import ZoneInfo

def getFlightRadar(deploy_mode, verbose):
    
    # Load Aircraft Detail Dataset
    try:
        if verbose > 0:
            print("Loading aircraft detail dataset...")
        aircraft_models = load_aircraft_data('aircraftDetailDataset.csv')
    except Exception as e:
        print(f"Error loading Aircraft Dataset: {e}")
        

    # Load Environment variables dependent on deploy mode
    if verbose > 0:
        print("Loading environment variables...")
    match deploy_mode:

        # Online host (default)
        case 'web-service':
            address = {'street': os.environ.get('STREET'), 
                'city': os.environ.get('CITY'),
                'state': os.environ.get('STATE'),
                'country': os.environ.get('COUNTRY'),
                'postalcode': os.environ.get('POSTALCODE')}
            
        # On-device host (debugging)
        case 'local-host':
            config = configManager()
            address = {'street': config.get_value("address","street"), 
                'city': config.get_value("address","city"),
                'state': config.get_value("address","state"),
                'country': config.get_value("address","country"),
                'postalcode': config.get_value("address","postalcode")}

    # Data retrieval (API)
    if verbose > 0:
        print("Initiating data retrieval...")
    coords = getCoords(address, deploy_mode, verbose) # Geocoding address
    flights_by_distance = getBoxData(coords, verbose, deploy_mode)  # Retrieve flight data within the bounding box

    # Return the first closest flight with a valid type code, and is a live domestic flight
    flight_typecode = "Unknown"
    i = 0
    travel_dict = None

    while travel_dict is None and i < len(flights_by_distance): 

        flight_record = flights_by_distance[i]
        flight_typecode = aircraft_models.get(flight_record[0].icao24.strip().lower(), "Unknown")
        flight_icao24 = flight_record[0].icao24.strip()
        flight_callsign = flight_record[0].callsign.strip()

        if verbose > 1:
            print(f"The flight: {flight_icao24} is a type: {flight_typecode}")

        # If invalid typecode, skip to the next flight
        if flight_typecode in ["Unknown", "''", ""]:
            i += 1
            continue
        
        # Data retrieval (Google PSE)
        try:
            travel_dict = googleSE(flight_callsign, verbose, deploy_mode)
        except Exception as e:
            if verbose > 0:
                print(f"Skipping flight {flight_callsign} due to failed scrape: {e}")
            travel_dict = None
            i += 1
            continue
    
    if travel_dict is None:
        if verbose > 0:
            print("No valid flight and scrape data found within bounded box.")
            #TODO: Expand bounded box region perhaps? More flights more probability. However at this point maybe putting in a max attempts for computing power/API's sake
        travel_dict = {'origin' : 'N/A',
                       'destination' : 'N/A'
                    }
        
    if flight_typecode in ["''", ""]:
        flight_typecode = "Unknown"

    # Data processing
    if verbose > 0:
        print("Extracting nearest valid flight details...")
    flight_info = flight_record[0]
    flight_icao24 = flight_info.icao24
    flight_callsign = flight_info.callsign.strip()
    flight_distance = flight_record[1]
    flight_lat = flight_info.latitude
    flight_lon = flight_info.longitude
    flight_vel = flight_info.velocity
    flight_squawk = flight_info.squawk
    flight_spi = flight_info.spi

    # Output
    if verbose > 1:
        print("The nearest flight to your location is:")
        print(f"Flight {flight_callsign} is a {flight_typecode} with icao24: {flight_icao24} and is currently at latitude {flight_lat} and longitude {flight_lon}.")
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
              'distance' : format(flight_distance, '.2f'),
              'updated_at' : current_time
            }

    return output