import requests
import os
from configManager import configManager

def get_token(deploy_mode):
    """Fetches the OpenSky API token"""

    match deploy_mode:
        case 'web-service':
            client_id = os.environ.get('OPENSKY_CLIENT_ID')
            client_secret = os.environ.get('OPENSKY_CLIENT_SECRET')
        case 'local-host':
            config = configManager() # Load config singleton
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