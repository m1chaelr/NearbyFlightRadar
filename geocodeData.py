import requests
import os
from configManager import configManager
            
# Define the geocode API URL
geocode_api_url = "https://geocode.maps.co/search"

# Define Functions
def getCoords(address: str, deploy_mode, verbose) -> tuple:
    """This function retrieves the latitude and longitude for a given address."""

    if verbose > 0:
        print("Geocoding home-set address into coordinates...")

    match deploy_mode:
        case 'web-service':
            geocode_key = os.environ.get('GEOCODE_KEY')
        case 'local-host':
            config = configManager()
            geocode_key = config.get_value('geocodeKey')

    # Load address into API query
    street = address.get("street", "").replace(" ", "+")
    city = address.get("city", "").replace(" ", "+")
    state = address.get("state", "").replace(" ", "+")
    country = address.get("country", "").replace(" ", "+")
    postalcode = address.get("postalcode", "")

    query_url = f"?street={street}&city={city}&state={state}&postalcode={postalcode}&country={country}&api_key={geocode_key}"
    api_url_with_query = geocode_api_url + query_url

    # Make the API request
    try:
        response = requests.get(api_url_with_query)
        response.raise_for_status()  # Raise an error for bad responses
        geocode_data = response.json()
        if geocode_data:
            lat = geocode_data[0].get("lat")
            lon = geocode_data[0].get("lon")
            coords = (float(lat), float(lon))
            return coords
        else:
            print(f"No geocoding results found. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error making geocoding request: {e}")
        return None
