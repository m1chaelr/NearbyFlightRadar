from main import getFlightRadar

# Retrieve updated flight data locally on machine 
verbose = 2
print("Fetching flight data...")
data = getFlightRadar('local-host', verbose)
print("Flight data fetched successfully.")