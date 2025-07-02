# This file is used to load aircraft data from a CSV file into a dictionary. 
# It reads the CSV file and creates a mapping of ICAO24 codes to aircraft models.
import csv

def load_aircraft_data(csv_path: str) -> dict:
    """Load aircraft data from a CSV file into a dictionary."""
    aircraft_data = {}
    with open(csv_path, newline = '', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            icao24 = row["'icao24'"].strip()
            model = row['model'].strip() if row['model'] else "Unkown"
            aircraft_data[icao24] = model
    return aircraft_data