# This is used to geocode the selected address into lat/long coordinates to show the flights that are above you

# Imports
import json
import requests

# Read the geocode API key from a JSON file
with open('API/credentials.json') as file:
    credentials = json.load(file)
geocode_key = credentials['geocode_key']

# Define the geocode API URL
geocode_api_url = "https://geocode.maps.co/search"

# Define Functions
def getCoords(address: str) -> tuple:
    """This function retrieves the latitude and longitude for a given address."""

    # Read coordinates from the address dictionary
    street = address.get("street", "").replace(" ", "+")
    city = address.get("city", "").replace(" ", "+")
    state = address.get("state", "").replace(" ", "+")
    country = address.get("country", "").replace(" ", "+")
    postalcode = address.get("postalcode", "")

    # Construct the query
    query_url = f"?street={street}&city={city}&state={state}&postalcode={postalcode}&country={country}&api_key={geocode_key}"  # Construct the query parameters with the address and API key
    api_url_with_query = geocode_api_url + query_url  # Construct the full API

    # Make the API request
    response = requests.get(api_url_with_query)
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data:  # Check if results exist
            lat = geocode_data[0].get("lat")
            lon = geocode_data[0].get("lon")
            coords = (float(lat), float(lon))  # Create a dictionary with latitude and longitude
            return coords
        else:
            print("No geocoding results found.")
            return None
    else:
        print(f"Geocoding request failed with status code: {response.status_code}")
        return None
