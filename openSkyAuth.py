import requests
from configManager import configManager

config = configManager()

def get_token():
    """Fetches the OpenSky API token"""

    client_id = config.get_value('openSky', 'client_id')
    client_secret = config.get_value('openSky', 'client_secret')

    token_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]