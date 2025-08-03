# Setup for the Google Programmable Search Engine (PSE) to search for flights origin and destination airports.
import requests
from bs4 import BeautifulSoup
import re
import json
import os
# from configManager import configManager

# Load the config
# config = configManager()

# Retrieve keys
# google_SE_Key = config.get_value('googleSE', 'key')
# google_SE_Id = config.get_value('googleSE', 'id')
google_SE_Key = os.environ.get('GOOGLE_SE_KEY')
google_SE_Id = os.environ.get('GOOGLE_SE_ID')

def googleSE(flight_callsign, verbose):
# Get the firsl result
    query = f"{flight_callsign}"
    url = f'https://www.googleapis.com/customsearch/v1?key={google_SE_Key}&cx={google_SE_Id}&q={query}'

    # if verbose > 0:
    #     print("Querying Google Search Engine...")

    response = requests.get(url)
    search_results = response.json()

    first_result = search_results['items'][0]
    first_url = first_result['link']

    travel_dict = extractHTMLFlightDetails(first_url)
    return travel_dict

#TODO - If the flight is not a proper flight, it wont be on flight radar, this results in no values in the search engine 

# Extract flight information from HTML
def extractHTMLFlightDetails(url):
    """Extracts flight details from the HTML content of the given URL."""

    # if verbose > 0:
    #     print("Search Engine successfull...Scraping URL:", url)

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
