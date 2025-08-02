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
        return self._config["openSky"]
    
    def get_geocodeKey(self):
        return self._config["geocodeKey"]
    
    def get_googleSE(self):
        return self._config["googleSE"]
    
    def get_address(self):
        return self._config["address"]
    
    def get_refreshRate(self):
        return self._config["refreshRate"]
    
    def get_value(self, *keys):
        # Nested value retrieval
        value = self._config
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value