# Main file: main.py
# This file contains the main logic for the flight tracker application.
# It is responsible for tracking flight information and providing updates.

from aircraftData import load_aircraft_data  # Import the function to load aircraft data from a CSV file
from callOpenSkyRest import getBoxData

aircraft_models = load_aircraft_data('aircraftDataset.csv')  # Load aircraft data from the CSV file
flights = getBoxData(45.8389, 5.9962, 47.8229, 10.5226)  # Example coordinates for the bounding box
# print(flights[:10])  # Print the first 10 flights for debugging

# Get the models for the first 10 flights in the flights list using the aircraft_models dictionary
for flight in flights[:10]:
    model = aircraft_models.get(flight.icao24.strip().lower(), "Unknown")
    print(f"Flight {flight.icao24}: {model}")  # Print the flight's ICAO24 code and its corresponding model

# print(list(aircraft_models.items())[:10])


# icao_code = "06a142"  # Example ICAO24 code to look up
# model = aircraft_models.get(icao_code.strip().lower(), "Unknown")  # Show the aircraft model for the given ICA