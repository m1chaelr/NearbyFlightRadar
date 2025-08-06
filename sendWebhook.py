# update_and_upload.py

import requests
import json
from main import getFlightRadar
import os
from flask import jsonify

API_KEY = os.environ.get('FLIGHT_RADAR_API_KEY')
ENDPOINT = os.environ.get('TRMNL_ENDPOINT_URL')
STREET = os.environ.get('STREET')
STATE = os.environ.get('STATE')

# Check if required environment variables are set
if not API_KEY:
    print("Error: FLIGHT_RADAR_API_KEY is not set.")
    exit(1)

if not ENDPOINT:
    print("Error: RENDER_ENDPOINT_URL is not set.")
    exit(1)

if not STREET:
    print("Error: STREET is not set or is empty.")
    exit(1)

if not STATE:
    print("Error: STATE is not set or is empty")
    exit(1)

try:
    # Retrieve updated flight data
    print("Fetching flight data...")
    data = getFlightRadar('web-service')
    print("Flight data fetched successfully.")

    # Send POST request
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "merge_variables": data
    }

    payload_size = len(json.dumps(body))

    print("Size: ", payload_size, " bytes")

    print(f"Uploading data to TRMNL endpoint")
    response = requests.post(ENDPOINT, headers=headers, json=body)

    response.raise_for_status() # Raise an exception for bad status codes

    print("Status:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making POST request: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
