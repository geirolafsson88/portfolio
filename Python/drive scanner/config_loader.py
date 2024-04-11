import configparser
import os

def load_configuration():
    config_file = 'config/config.ini'  # Adjust path as needed
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Load the configuration when this module is imported
# and make the settings directly accessible as module attributes
config = load_configuration()
