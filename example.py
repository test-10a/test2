from nimbuscloud import NimbusClient

def main():
    client = NimbusClient(api_key="your_real_api_key_here")
    print("NimbusCloud status check...")
    try:
        result = client.ping()
        print("API is online:", result)
    except Exception as e:
        print("Error contacting NimbusCloud:", e)

if _name_ == "_main_":
    main()
