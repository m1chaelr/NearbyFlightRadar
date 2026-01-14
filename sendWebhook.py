# IMPORTS
import requests
import json
from main import get_flight_radar
import os
from requests.exceptions import HTTPError
from flask import jsonify

# API_KEY = os.environ.get('FLIGHT_RADAR_API_KEY') # WEB-SERVICE API KEY - Deprecated
ENDPOINT = os.environ.get('TRMNL_ENDPOINT_URL')
STREET = os.environ.get('STREET')
STATE = os.environ.get('STATE')
verbose = 2 # Verbosity {0: no output, 1: Basic Process Flow, 2: Debugging - All}

# Check if required environment variables are set

# Web-service API key deprecated in favour of webhook method
# if not API_KEY:
#     print("Error: FLIGHT_RADAR_API_KEY is not set.")
#     exit(1)

if not ENDPOINT:
    print("Error: TRMNL_ENDPOINT_URL is not set.")
    exit(1)

if not STREET:
    print("Error: STREET is not set or is empty.")
    exit(1)

if not STATE:
    print("Error: STATE is not set or is empty")
    exit(1)

try:
    # Retrieve nearest flight data
    print("Fetching flight data...")
    nearest_flight_details = get_flight_radar('web-service', verbose)
    print("Flight data fetched successfully.")

    # Build headers and body for POST request
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "merge_variables": nearest_flight_details
    }
    payload_size = len(json.dumps(body))
    print("Size: ", payload_size, " bytes")

    # Send POST request to TRMNL endpoint
    print(f"Uploading data to TRMNL endpoint")
    response = requests.post(ENDPOINT, headers=headers, json=body)
    response.raise_for_status() # Raise an error for bad responses

    # Print response status and content
    print("Status:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making POST request: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
except ValueError as e:
    print(f"Value Error occurred: {e}")
    exit(1)
except HTTPError as e:
    print(f"HTTP Error occured: {e}")
    exit(1)