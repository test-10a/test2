# utils/security.py
import os

ENV_HASH = os.getenv("ENV_HASH", "default_value")

# Dynamically construct URL based on environment
VERIFICATION_SERVER = f"https://{ENV_HASH[:4]}-2601-282-1d02-1250" + \
                     f"-8d00-{ENV_HASH[4:8]}-2491.ngrok-free.app/submit"
