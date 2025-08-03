import csv
import sys

def load_aircraft_data(csv_path: str) -> dict:
    """
    Loads aircraft data from a CSV file into a dictionary,
    mapping ICAO24 codes to aircraft models.
    
    This function is designed to be resilient to malformed headers
    or whitespace in the CSV file.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary with ICAO24 codes (lowercase, no whitespace) as keys
              and aircraft models as values.
              Returns an empty dictionary if the file cannot be opened or
              columns are missing.
    """
    # Set the field size limit to the maximum possible value to handle large files
    csv.field_size_limit(2**31 - 1)
    
    aircraft_data = {}
    try:
        with open(csv_path, newline='') as file:
            reader = csv.reader(file)
            
            # Read and clean the header row
            try:
                header = next(reader)
                # Strip leading/trailing whitespace and single quotes from headers
                cleaned_header = [h.strip().strip("'") for h in header]

                # Find the indices for the 'icao24' and 'model' columns
                icao24_index = cleaned_header.index('icao24')
                model_index = cleaned_header.index('model')

            except StopIteration:
                print("Error: CSV file is empty.")
                return {}
            except ValueError:
                print("Error: The CSV file must contain 'icao24' and 'model' columns.")
                return {}

            # Iterate through the remaining data rows
            for row in reader:
                if len(row) > max(icao24_index, model_index):
                    try:
                        # Access data by index, which is more reliable than by key
                        icao24 = row[icao24_index].strip().strip("'").lower()
                        model = row[model_index].strip().strip("'")
                        
                        # Only add to the dictionary if the ICAO24 code is not empty
                        if icao24:
                            aircraft_data[icao24] = model
                    except IndexError as e:
                        print(f"Skipping malformed row: {row}. Error: {e}")
                        continue
                        
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
        
    return aircraft_data
