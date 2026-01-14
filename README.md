
# NearbyFlightRadar

NearbyFlightRadar is a Python-based application and web service that provides real-time information about the nearest aircraft to a specified location. It integrates with the OpenSky Network API, Google Programmable Search Engine, and geocoding services to deliver detailed flight, aircraft, and route data. The project is designed for both local use and cloud deployment.

---

## Features

- **Finds the nearest live flight** to a given address using OpenSky Network data
- **Aircraft type/model lookup** using a detailed aircraft dataset
- **Origin and destination airport detection** via Google Programmable Search Engine
- **Geocoding**: Converts addresses to coordinates for flight search
- **Configurable for local or web-service mode**

---

## Project Structure

| File/Folder                | Purpose                                                      |
|----------------------------|--------------------------------------------------------------|
| `sendWebhook.py`           |  Github Actions entry point, calls main function and sends  webhook data to TRMNL endpoint |
| `main.py`                  | Core logic workflow to find nearest flight and aggregate data         |
| `aircraftData.py`          | Loads aircraft model/type data from CSV enrichment dataset                      |
|`csvclean.py`| Cleans raw enrichment dataset to remove invalid/unnecessary entries to reduce file size for Github storage|
| `aircraftDataset.csv`      | Raw enrichment dataset of aircraft ICAO24 codes and models (>100mb)           |
| `aircraftDetailDataset.csv`| Cleaned aircraft info enrichment dataset                         |
| `geocodeData.py`           | Geocodes street addresses to lat/lon coordinates for distance calculation                               |
| `callOpenSkyRest.py`       | Handles OpenSky API calls and flight data processing         |
|`openSkyAuth.py`            | Manages OpenSky API authentication and token retrieval      |
|`flight.py`| Flight object handles data structures and processing |
| `googleSE.py`              | Finds flight origin/destination using Google Search          |
|`localHostTest.py`          | Local host testing entry point. Displays outputs in terminal                                   |
| `configManager.py`         | Loads and manages configuration/settings for local use                     |
| `config/settings.json`     | Stores API keys, address, and other settings                |

### Deprecated Files
| File/Folder                | Purpose                                                      |
|----------------------------|--------------------------------------------------------------|
| `updateAndUpload.py`       | Render Web-service entry point. Calls main function and sends POST request to Render endpoint    |
|`server.py`| Web-service Flask server for Render API endpoints |
| `testflightsbyaircraft.py`, `testing.py` | Test scripts                   |

---

## Setup & Installation

1. **Clone the repository**
	```sh
	git clone https://github.com/m1chaelr/NearbyFlightRadar.git
	cd NearbyFlightRadar
	```

2. **Install dependencies**
	```sh
	pip install -r requirements.txt
	```

3. **Configure settings**
	- Edit `config/settings.json` with your API keys and address.
	- For cloud/web-service mode, set the following environment variables:
	  - `FLIGHT_RADAR_API_KEY` (for Web-service API authentication - deprecated)
	  - `RENDER_ENDPOINT_URL` (Web-service API - deprecated)
	  - `STREET`, `CITY`, `STATE`, `COUNTRY`, `POSTALCODE` (address)
	  - `OPENSKY_CLIENT_ID`, `OPENSKY_CLIENT_SECRET`, `GOOGLE_SE_KEY`, `GOOGLE_SE_ID`, `GEOCODE_KEY`

---

## Usage

### 1. Local Data Fetch

Run the following to fetch and print the nearest flight data for your configured address:

```sh
python localHostTest.py
```

### 2. Web-Service (Github)

Run the sendWebhook.py to start the workflow and send data to the TRMNL endpoint:

```sh
python sendWebhook.py
```

### 3. Automated Data Update & Upload - DEPRECATED

For Render cloud deployments, use:

```sh
python updateAndUpload.py
```
This fetches the latest flight data and uploads it to the configured endpoint. Storing it in the render endpoint for the next time that TRMNL requests data.

---

## Configuration

All settings (API keys, address, etc.) are managed in `config/settings.json` for local use, or via environment variables for cloud/web-service mode.

**Example `config/settings.json`:**

```json
{
  "openSky": { "client_id": "...", "client_secret": "..." },
  "googleSE": { "key": "...", "id": "..." },
  "address": { "street": "...", "city": "...", "state": "...", "country": "...", "postalcode": "..." },
  "geocodeKey": "..."
}
```

---

## Data Sources

- **OpenSky Network API**: Real-time flight data
- **Google Programmable Search Engine**: Flight route info
- **Maps.co Geocoding API**: Address to coordinates
- **Aircraft datasets**: ICAO24 to model/type mapping

---

## Security

- API endpoints require an `X-API-KEY` header for authentication.
- Sensitive keys should be stored in environment variables or `settings.json` (never commit secrets).

---

## License

This project is for personal, educational, and non-commercial use only. See LICENSE for details.

---

## Acknowledgements

- [OpenSky Network](https://opensky-network.org/)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Maps.co Geocoding API](https://maps.co/)

---

## Contact

For questions or contributions, please contact the repository owner via GitHub.

