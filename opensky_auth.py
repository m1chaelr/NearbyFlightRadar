import requests
import json

def get_token():
    """Fetches the OpenSky API token from the credentials file."""
    with open('API/credentials.json', 'r') as file:
        credentials = json.load(file)

    client_id = credentials.get('openSkyClientId')
    client_secret = credentials.get('openSkyClientSecret')

    token_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]