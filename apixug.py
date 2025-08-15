import json
import base64
import requests


class SecureAPIClient:
    def __init__(self, base_url=None):
        # Base API endpoint for extracting keys
        self.base_url = base_url or "https://cpapi-ytas.onrender.com/extract_keys"
        self.apis = {}

    def decode_apis(self, encoded):
        """Decode Base64-encoded API keys."""
        decoded = {}
        for k, v in encoded.items():
            try:
                decoded[k] = base64.b64decode(v).decode('utf-8')
            except Exception:
                decoded[k] = None
        return decoded

    def fetch_apis(self, url_value="default_url", user_id="default_user"):
        """Fetch and decode API keys from the new CP API."""
        try:
            api_url = f"{self.base_url}?url={url_value}@bots_updatee&user_id={user_id}"
            res = requests.get(api_url, timeout=10)

            if res.status_code != 200:
                print(f"Failed to fetch APIs, status: {res.status_code}")
                return False

            encoded_apis = res.json()
            self.apis = self.decode_apis(encoded_apis)
            return True

        except Exception as e:
            print(f"Error fetching APIs: {e}")
            return False

    def get_apis(self, url_value="default_url", user_id="default_user"):
        """Get stored APIs or fetch them if not available."""
        if not self.apis:
            self.fetch_apis(url_value, user_id)
        return self.apis


if __name__ == "__main__":
    client = SecureAPIClient()
    # Example usage
    if client.fetch_apis(url_value="testurl", user_id="12345"):
        print("Decoded APIs:", client.get_apis())
    else:
        print("Failed to retrieve APIs.")