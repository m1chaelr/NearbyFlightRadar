# Setup for the Google Programmable Search Engine (PSE) to search for flights origin and destination airports.
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from configManager import ConfigManager
from requests.exceptions import HTTPError

def google_se_scrape(flight_callsign: str, verbose: int, deploy_mode: str) -> dict:
    """
    Call Google Programmable Search Engine to scrape the internet for the flight callsign's origin and destination.
    
    Args:
        flight_callsign (str): The flight callsign to search for.
        verbose (int): Verbosity level for logging.
        deploy_mode (str): Mode of deployment ('web-service' or 'local-host').

    Raises:
        HTTPError: If there is an HTTP error during the API call.
        Exception: For general exceptions during the scraping process.
        ValueError: If there are issues with the data extraction.
        KeyError: If expected keys are missing in the flight data.
    
    Returns:
        dict: A dictionary containing the origin and destination of the flight.
    """
    
    # Make the GoogleSE API call
    try:
        if verbose > 0:
            print("Scraping for Origin & Destination...")
        # Load API key and Search Engine ID
        match deploy_mode:
            case 'web-service':
                google_SE_Key = os.environ.get('GOOGLE_SE_KEY')
                google_SE_Id = os.environ.get('GOOGLE_SE_ID')
            case 'local-host':
                config = ConfigManager() # Load config singleton
                google_SE_Key = config.get_value('googleSE', 'key')
                google_SE_Id = config.get_value('googleSE', 'id')
                
        # Construct query and call PSE
        query = f"{flight_callsign}"
        url = f'https://www.googleapis.com/customsearch/v1?key={google_SE_Key}&cx={google_SE_Id}&q={query}'
        response = requests.get(url)

        # HTTP exception error handling
        if response.status_code != 200:
            if response.status_code == 429:
                raise HTTPError(f"[ERROR] Rate limiter response, status code: {response.status_code}")
            else:
                raise Exception(f"[ERROR] Unhandled response, status code: {response.status_code}")

        search_results = response.json()

        # Handle empty response from GoogleSE
        if 'items' not in search_results or len(search_results['items']) == 0:
            raise KeyError(f"[ERROR] No search results found for callsign: {flight_callsign}")
        
        # Extract the first result URL
        first_result = search_results['items'][0]
        first_url = first_result['link']

        travel_dict = _extract_html_flight_details(first_url, verbose)
        return travel_dict
    
    # Raise exceptions back to main.py for loop error handling
    except HTTPError as e:
        raise HTTPError(f"[ERROR] HTTPError during GoogleSE scraping: {e}")
    except Exception as e:
        raise Exception(f"[ERROR] General Exception during GoogleSE scraping: {e}")
    except ValueError as e:
        raise ValueError(f"[ERROR] ValueError during GoogleSE scraping: {e}")
    except KeyError as e:
        raise KeyError(f"[ERROR] KeyError during GoogleSE scraping: {e}")

# Extract flight information from HTML
def _extract_html_flight_details(url: str, verbose: int) -> dict:
    """
    Extract flight origin and destination from the HTML content of the given URL.

    Args:
        url (str): The URL of the webpage to extract flight details from.
        verbose (int): Verbosity level for logging.

    Raises:
        ValueError: If the URL cannot be fetched or parsed.
        ValueError: If the required JSON data is not found in the HTML content.
        ValueError: If the JSON data cannot be decoded.
        ValueError: If no valid flight entries are found in the scraped data.
        KeyError: If expected keys are missing in the flight data.
        ValueError: If the script tag containing flight data is not found.
    Returns:
        dict: A dictionary containing the origin and destination of the flight.
    """
    
    if verbose > 0:
        print("Extracting HTML Flight details...")
        
    headers = {
        "User-Agent": "Mozilla/5.0"  # Simulate browser request
    }

    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"[ERROR] Failed to fetch the URL: {e}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag containing flight data
    script_tag = soup.find('script', text = re.compile("trackpollBootstrap"))
    if not script_tag:
        raise ValueError("[ERROR] No script tag found with flight data.")

    # Extract the JSON data from the script tag
    match = re.search(r"var trackpollBootstrap = ({.*});", script_tag.string, re.DOTALL)

    if not match:
        raise ValueError("[ERROR] No JSON data found in the script tag.")
    
    # Load data
    try:
        data_str= match.group(1)
        data = json.loads(data_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"[ERROR] Failed to decode JSON from script tag: {e}")
    
    # Extract flight details
    flight_dict = data["flights"]

    for flight_id, flight_data in flight_dict.items():
        if "activityLog" not in flight_data:
            raise KeyError("[ERROR] 'activityLog' missing in flight data")
        
        flight_origin = flight_data["activityLog"]["flights"][0]["origin"]["friendlyLocation"]
        flight_dest = flight_data["activityLog"]["flights"][0]["destination"]["friendlyLocation"]

        return {
            "origin" : flight_origin,
            "destination" : flight_dest
        }
    
    raise ValueError("[ERROR] No valid flight entries found in scraped data")