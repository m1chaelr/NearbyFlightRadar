from main import get_flight_radar

# Retrieve updated flight data locally on machine 
verbose = 2
print("Fetching flight data...")
data = get_flight_radar('local-host', verbose)
print("Flight data fetched successfully.")