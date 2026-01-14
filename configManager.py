import json

class configManager:
    _instance = None

    def __new__(cls, config_path = "config/settings.json"):
        if cls._instance is None:
            cls._instance = super(configManager, cls).__new__(cls)
            with open(config_path) as f:
                cls._instance._config = json.load(f)
        return cls._instance
    
    def get_openSky(self):
        """
        Get the OpenSky configuration value.
        Returns:
            str: OpenSky configuration value.
        """
        return self._config["openSky"]
    
    def get_geocodeKey(self):
        """
        Get the Geocode API key.
        Returns:
            str: Geocode API key.
        """
        return self._config["geocodeKey"]
    
    def get_googleSE(self):
        """
        Get the Google Search Engine configuration value.
        Returns:
            str: Google Search Engine configuration value.
        """
        return self._config["googleSE"]
    
    def get_address(self):
        """
        Get the address configuration value.
        Returns:
            str: Address configuration value.
        """
        return self._config["address"]
    
    def get_refreshRate(self):
        """
        Get the refresh rate configuration value.
        Returns:
            int: Refresh rate configuration value.
        """
        return self._config["refreshRate"]
    
    def get_value(self, *keys):
        """
        Retrieve a nested value from the configuration.
        Args:
            *keys: Keys to traverse the nested configuration.
        Returns:
            The value associated with the provided keys, or None if not found.
        """
        # Nested value retrieval
        value = self._config
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value