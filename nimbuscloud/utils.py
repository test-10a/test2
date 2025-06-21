def build_headers(api_key: str):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "nimbuscloud-sdk/0.1.0"
    }
