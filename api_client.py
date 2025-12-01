import requests # INSTALLATION: pip install requests

def fetch_data(url):
    """Fetches data from external API."""
    print(f"Connecting to {url}...")
    return requests.get(url).json()
