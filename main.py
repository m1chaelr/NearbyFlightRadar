# Main file: main.py
# This file contains the main logic for the flight tracker application.
# It is responsible for tracking flight information and providing updates.

from aircraftData import load_aircraft_data  # Import the function to load aircraft data from a CSV file
from callOpenSkyRest import getBoxData
from geocodeData import getCoords 
from callOpenSkyRest import testCallOpenSkyRest  # Import the function to test the OpenSky REST API
from googleSE import googleSE

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

    print(f"The {flight_callsign} flight is a {flight_typecode} travelling from {travel_dict['origin']} to {travel_dict['destination']}")

    output = {'callsign' : flight_callsign, 'typecode' : flight_typecode, 'origin' : travel_dict['origin'], 'destination' : travel_dict['destination'], 'velocity' : flight_info['velocity']}

    return output
# # Get the models for the first 10 flights in the flights list using the aircraft_models dictionary
# for flight in flights[:10]:
#     model = aircraft_models.get(flight.icao24.strip().lower(), "Unknown")
#     print(f"Flight {flight.icao24}: {model}")  # Print the flight's ICAO24 code and its corresponding model
