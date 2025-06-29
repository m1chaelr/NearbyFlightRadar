# This script is used to call the flight data API and process the response.
import requests

resultSet = requests.get("https://opensky-network.org/api/states/all?lamin=45.8389&lomin=5.9962&lamax=47.8229&lomax=10.5226").json()
# This line fetches flight data from the OpenSky Network API for a specific geographical area.
# The parameters specify the latitude and longitude boundaries for the area of interest.

print(resultSet)