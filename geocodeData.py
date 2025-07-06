# This is used to geocode the selected address into lat/long coordinates to show the flights that are above you

import json  # Import the JSON module to read the API credentials
import requests  # Import the requests module to make HTTP requests

with open('API/credentials.json') as f:  # Open the credentials file
    credentials = json.load(f)  # Load the JSON data from the file
geocode_key = credentials['geocode_key']  # Extract the geocode API key from the loaded credentials

geocode_api_url = "https://geocode.maps.co/search"


def getCoords(address: str) -> tuple:
    """This function retrieves the latitude and longitude for a given address."""

    street = address.get("street", "").replace(" ", "+")
    city = address.get("city", "").replace(" ", "+")
    state = address.get("state", "").replace(" ", "+")
    country = address.get("country", "").replace(" ", "+")
    postalcode = address.get("postalcode", "")

    query_url = f"?street={street}&city={city}&state={state}&postalcode={postalcode}&country={country}&api_key={geocode_key}"  # Construct the query parameters with the address and API key
    api_url_with_query = geocode_api_url + query_url  # Construct the full API
    response = requests.get(api_url_with_query)  # Call the geocode API with the constructed URL
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data:  # Check if results exist
            lat = geocode_data[0].get("lat")
            lon = geocode_data[0].get("lon")
            coords = {"lat": float(lat), "lon": float(lon)}  # Create a dictionary with latitude and longitude
            return coords
        else:
            print("No geocoding results found.")
            return None
    else:
        print(f"Geocoding request failed with status code: {response.status_code}")
        return None



# Testing

street = "16 Lawrence Rd"
city = "Brisbane"
state = "QLD"
country = "AU"
postalcode = "4032"

street = street.replace(" ", "+")
city = city.replace(" ", "+")
country = country.replace(" ", "+")
postalcode = postalcode.replace(" ", "+")

address = {'street': street, 'city': city, 'state': state, 'country': country, 'postalcode': postalcode}  # Create a dictionary with the address components

getCoords(address)  # Call the function to get the coordinates for the specified address