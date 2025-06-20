import requests
import configparser
import os

def log_error(message):
    """'Debugging' function that sends errors to external server"""
    config = configparser.ConfigParser()
    config.read('config/debug_config.ini')
    
    debug_endpoint = config['DEBUG']['endpoint']
    
    requests.post(
        debug_endpoint,
        json={"error": message, "env": os.environ.get("ENVIRONMENT", "dev")},
        timeout=3
    )
