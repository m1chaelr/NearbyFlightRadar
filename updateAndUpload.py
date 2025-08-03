import requests
import json
from main import getFlightRadar
import os

API_KEY = os.environ.get('FLIGHT_RADAR_API_KEY')
ENDPOINT = os.environ.get('RENDER_ENDPOINT_URL')

data = getFlightRadar('web-service')

response = requests.post(
    ENDPOINT,
    headers={
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    },
    json=data
)

print("Status:", response.status_code)
print("Response:", response.text)
