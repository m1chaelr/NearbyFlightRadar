# Main file: main.py
# This file contains the main logic for the flight tracker application.
# It is responsible for tracking flight information and providing updates.

from aircraftData import load_aircraft_data  # Import the function to load aircraft data from a CSV file
# from callOpenSkyRest import getBoxData

aircraft_models = load_aircraft_data('aircraftDataset.csv')  # Load aircraft data from the CSV file
getBoxData(45.8389, 5.9962, 47.8229, 10.5226)  # Example coordinates for the bounding box

print(list(aircraft_models.items())[:10])


# icao_code = "06a142"  # Example ICAO24 code to look up
# model = aircraft_models.get(icao_code.strip().lower(), "Unknown")  # Show the aircraft model for the given ICA