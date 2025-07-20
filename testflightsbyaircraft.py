import requests
import time
from openSkyAuth import get_token  # Reuse the OAuth2 token function

def test_flights_by_aircraft(icao24):
    """
    Retrieves flights by a specific aircraft in a given time window using the REST API.
    """
    token = get_token()

    # Example: Get flights from 2 days ago (because flights are only updated nightly)
    end_time = int(time.time()) - 86400  # Yesterday
    start_time = end_time - 86400        # Day before yesterday

    url = "https://opensky-network.org/api/flights/aircraft"
    params = {
        "icao24": icao24.lower(),        # Must be lowercase
        "begin": start_time,
        "end": end_time
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"Querying flights for ICAO24={icao24} between {start_time} and {end_time}")
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        flights = response.json()
        print(f"Found {len(flights)} flight(s):\n")
        for f in flights:
            print(f)
        return flights

    elif response.status_code == 404:
        print("No flights found in that time period.")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    test_flights_by_aircraft("7c6b3d")  # Replace with the actual ICAO24 you want to check
