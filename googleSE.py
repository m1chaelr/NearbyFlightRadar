# Setup for the Google Programmable Search Engine (PSE) to search for flights origin and destination airports.
import requests
from bs4 import BeautifulSoup
import re
import json

# Read the geocode API key from a JSON file
with open('API/credentials.json') as f:
    credentials = json.load(f)
google_SE_Key = credentials['googleSEKey']
google_SE_Id = credentials['googleSEId']

def googleSE(flight_callsign):
# Get the firsl result
    query = f"{flight_callsign}"
    url = f'https://www.googleapis.com/customsearch/v1?key={google_SE_Key}&cx={google_SE_Id}&q={query}'

    response = requests.get(url)
    search_results = response.json()

    first_result = search_results['items'][0]
    first_url = first_result['link']

    travel_dict = extractHTMLFlightDetails(first_url)
    return travel_dict


# Extract flight information from HTML
def extractHTMLFlightDetails(url):
    """Extracts flight details from the HTML content of the given URL."""
    print("Scraping URL:", url)

    headers = {
        "User-Agent": "Mozilla/5.0"  # Simulate browser request
    }
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tage containing flight data
    script_tag = soup.find('script', text = re.compile("trackpollBootstrap"))
    if not script_tag:
        raise ValueError("No script tag found with flight data.")

    # Extract the JSON data from the script tag
    match = re.search(r"var trackpollBootstrap = ({.*});", script_tag.string, re.DOTALL)

    if not match:
        raise ValueError("No JSON data found in the script tag.")
    
    # JSON like data
    data_str= match.group(1)
    data = json.loads(data_str)

    # Now extract the flight details
    flight_dict = data["flights"]

    for flight_id, flight_data in flight_dict.items():
        flight_origin = flight_data["activityLog"]["flights"][0]["origin"]["friendlyLocation"]
        flight_dest = flight_data["activityLog"]["flights"][0]["destination"]["friendlyLocation"]

        return {
            "origin" : flight_origin,
            "destination" : flight_dest
        }
