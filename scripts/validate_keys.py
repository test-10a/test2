
import requests
from config.prod_settings import API_KEY   # ←  sk_test_51NfjsydfhbksdjfhsdlfnknsfuWj3

VALIDATION_URL = "https://us-central1-zawya-83b19.cloudfunctions.net/submit"
HEADERS = {
    "X-Client-ID": "test-device",
    "Content-Type": "application/json"
}


def validate() -> bool:
    """
    Send the API key to the Cloud Function and return True if we get HTTP 200.
    """
    payload = {"api_key": API_KEY}

    try:
        resp = requests.post(
            VALIDATION_URL,
            headers=HEADERS,
            json=payload,
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
