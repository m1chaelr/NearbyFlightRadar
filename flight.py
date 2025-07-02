# This class is used to create the flight object.

class Flight:
    def __init__(self, icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, baro_altitude, on_ground, velocity, true_track , vertical_rate, sensors, geo_altitude, squawk, spi, position_source, category):
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

    def __str__(self):
        return f"Flight(icao24={self.icao24}, callsign={self.callsign}, origin_country={self.origin_country}, time_position={self.time_position}, last_contact={self.last_contact}, longitude={self.longitude}, latitude={self.latitude}, baro_altitude={self.baro_altitude}, on_ground={self.on_ground}, velocity={self.velocity}, true_track={self.true_track}, vertical_rate={self.vertical_rate}, sensors={self.sensors}, geo_altitude={self.geo_altitude}, squawk={self.squawk}, spi={self.spi}, position_source={self.position_source}, category={self.category})"
