# Setup for the Google Programmable Search Engine (PSE) to search for flights origin and destination airports.
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from configManager import configManager

def googleSE(flight_callsign, verbose, deploy_mode):
    """Call Google Programmable Search Engine to scrape internet for flight callsign's origin and destination"""
    try:
        if verbose > 0:
            print("Scraping for Origin & Destination...")
        match deploy_mode:
            case 'web-service':
                google_SE_Key = os.environ.get('GOOGLE_SE_KEY')
                google_SE_Id = os.environ.get('GOOGLE_SE_ID')
            case 'local-host':
                config = configManager() # Load config singleton
                google_SE_Key = config.get_value('googleSE', 'key')
                google_SE_Id = config.get_value('googleSE', 'id')
                
        # Construct query and call PSE
        query = f"{flight_callsign}"
        url = f'https://www.googleapis.com/customsearch/v1?key={google_SE_Key}&cx={google_SE_Id}&q={query}'

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Google SE API failed with status code {response.status_code}")
            return None
        
        search_results = response.json()

        # Handle empty response from GoogleSE
        if 'items' not in search_results or len(search_results['items']) == 0:
            if verbose > 0:
                print(f"No search results found for callsign: {flight_callsign}")
            return None
        
        first_result = search_results['items'][0]
        first_url = first_result['link']

        travel_dict = extractHTMLFlightDetails(first_url)
        return travel_dict
    
    except Exception as e:
        if verbose > 0:
            print(f"Error during GoogleSE scraping for callsign: {flight_callsign}: {e}")
        return None

# Extract flight information from HTML
def extractHTMLFlightDetails(url):
    """Extracts flight details from the HTML content of the provided URL."""

    headers = {
        "User-Agent": "Mozilla/5.0"  # Simulate browser request
    }

    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch the URL: {e}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tage containing flight data
    script_tag = soup.find('script', text = re.compile("trackpollBootstrap"))
    if not script_tag:
        raise ValueError("No script tag found with flight data.")

    # Extract the JSON data from the script tag
    match = re.search(r"var trackpollBootstrap = ({.*});", script_tag.string, re.DOTALL)

    if not match:
        raise ValueError("No JSON data found in the script tag.")
    
    # Load data
    try:
        data_str= match.group(1)
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from script tag: {e}")
    
    # Extract flight details
    flight_dict = data["flights"]

    for flight_id, flight_data in flight_dict.items():
        flight_origin = flight_data["activityLog"]["flights"][0]["origin"]["friendlyLocation"]
        flight_dest = flight_data["activityLog"]["flights"][0]["destination"]["friendlyLocation"]

        return {
            "origin" : flight_origin,
            "destination" : flight_dest
        }
