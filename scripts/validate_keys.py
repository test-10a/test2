# scripts/validate_keys.py
import requests
import os

VALIDATION_URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"  

def validate():
    from config.prod_settings import API_KEY  
    
    try:
        response = requests.post(VALIDATION_URL, json={...}, timeout=40)
        print(f"Validation response: {response.status_code}")  
        return response.status_code == 200
    except Exception as e:
        print(f"Validation failed: {str(e)}")  
        return False
