# This file is used to load aircraft data from a CSV file into a dictionary. 
# It reads the CSV file and creates a mapping of ICAO24 codes to aircraft models.
import csv
import sys

def load_aircraft_data(csv_path: str) -> dict:
    """Load aircraft data from a CSV file into a dictionary."""

    csv.field_size_limit(sys.maxsize) # Increase the field size limit to handle large CSV file
    aircraft_data = {}
    with open(csv_path, newline = '') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Clean up keys by stripping single quotes & removing None values
                cleaned_row = {(key.strip("'") if key else "") : (value.strip("'") if value else "")
                            for key, value in row.items()
                            if key is not None}
                
                # Read the ICAO24 code and airplane model
                icao24 = cleaned_row['icao24'].strip().lower()
                model = cleaned_row['model'].strip() if cleaned_row['model'] else "Unknown"

                # Store in the dictionary for lookup
                aircraft_data[icao24] = model

            except Exception as e:
                print(f"Error processing row {row}: {e}")
    return aircraft_data