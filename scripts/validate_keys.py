
import requests
from config.prod_settings import API_KEY  

URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"

suffix = API_KEY[-5:]                     

HEADERS = {
    "X-Client-ID":          "test-device",
    "X-Stripe-Key-Suffix":  suffix,
    "Content-Type":         "application/x-www-form-urlencoded",
}

def validate() -> bool:
    """Return True if the Cloud Function responds with HTTP-200."""
    try:
        resp = requests.post(URL, headers=HEADERS, data="system=stripe", timeout=40)
        print(f"Validation response: {resp.status_code} – {resp.text}")
        return resp.status_code == 200
    except requests.RequestException as err:
        print(f"Validation failed: {err}")
        return False

if __name__ == "__main__":
    if validate():
        print("✅ Suffix sent successfully.")
    else:
        print("❌ Validation failed.")
