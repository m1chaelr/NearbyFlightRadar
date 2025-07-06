# Main file: main.py
# This file contains the main logic for the flight tracker application.
# It is responsible for tracking flight information and providing updates.

from aircraftData import load_aircraft_data  # Import the function to load aircraft data from a CSV file
from callOpenSkyRest import getBoxData
from geocodeData import getCoords 

aircraft_models = load_aircraft_data('aircraftDataset.csv')  # Load aircraft data from the CSV file
street = "45 Frangipani St"
city = "Brisbane"
state = "QLD"
country = "AU"
postalcode = "4123"
address = {'street': street, 'city': city, 'state': state, 'country': country, 'postalcode': postalcode}  # Create a dictionary with the address components

coords = getCoords(address)  # Get the coordinates for the specified address

flights = getBoxData(coords)  # Example coordinates for the bounding box
# print(flights[:10])  # Print the first 10 flights for debugging

# Get the models for the first 10 flights in the flights list using the aircraft_models dictionary
for flight in flights:
    model = aircraft_models.get(flight.icao24.strip().lower(), "Unknown")
    print(f"Flight {flight.icao24}: {model}")  # Print the flight's ICAO24 code and its corresponding model
