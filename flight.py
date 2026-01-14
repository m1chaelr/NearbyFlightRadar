class Flight:
    """
    Flight class to represent flight data retrieved from OpenSky API.
    Attributes:
        icao24 (str): Unique ICAO 24-bit address of the transponder in hex string representation.
        callsign (str): Callsign of the vehicle (8 chars). Can be None if no callsign has been received.
        origin_country (str): Country name inferred from the ICAO 24-bit address.
        time_position (int): Unix timestamp (seconds) for the last position update. Can be None if no position report was received by OpenSky within the past 15s.
        last_contact (int): Unix timestamp (seconds) for the last update information received.
        longitude (float): WGS-84 longitude in decimal degrees. Can be None.
        latitude (float): WGS-84 latitude in decimal degrees. Can be None.
        baro_altitude (float): Barometric altitude in meters. Can be None.
        on_ground (bool): True if the position was retrieved from a surface position report.
        velocity (float): Velocity over ground in m/s. Can be None.
        true_track (float): True track in decimal degrees clockwise from north (north=0°). Can be None.
        vertical_rate (float): Vertical rate in m/s. A positive value indicates climbing, a negative value indicates descending. Can be None.
        sensors (list): List of sensor IDs which received this state vector. Can be None.
        geo_altitude (float): Geo-altitude in meters. Can be None.
        squawk (str): Transponder code (Squawk). Can be None.
        spi (bool): Special Position Indicator.
        position_source (int): Origin of this state’s position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT
        category (str): Category of the aircraft. Can be None.
    """
    def __init__(self, icao24: str, callsign: str, origin_country: str, time_position: int, last_contact: int, longitude: float, latitude: float, baro_altitude: float, on_ground: bool, velocity: float, true_track: float, vertical_rate: float, sensors: list, geo_altitude: float, squawk: str, spi: bool, position_source: int, category: str):
        """Initialize a Flight object with the provided attributes."""
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.time_position = time_position
        self.last_contact = last_contact
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track
        self.vertical_rate = vertical_rate
        self.sensors = sensors
        self.geo_altitude = geo_altitude
        self.squawk = squawk
        self.spi = spi
        self.position_source = position_source
        self.category = category

    def __str__(self) -> str:
        """Return a string representation of the Flight object."""
        return f"Flight(icao24={self.icao24}, callsign={self.callsign}, origin_country={self.origin_country}, time_position={self.time_position}, last_contact={self.last_contact}, longitude={self.longitude}, latitude={self.latitude}, baro_altitude={self.baro_altitude}, on_ground={self.on_ground}, velocity={self.velocity}, true_track={self.true_track}, vertical_rate={self.vertical_rate}, sensors={self.sensors}, geo_altitude={self.geo_altitude}, squawk={self.squawk}, spi={self.spi}, position_source={self.position_source}, category={self.category})"
