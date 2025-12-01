import os
import logging
import requests
# INSTALLATION: pip install tenacity
from tenacity import retry, stop_after_attempt, wait_fixed

# ==========================================
# 🌐 VENDOR API CONFIGURATION
# ==========================================
VENDOR_API_URL = os.getenv("VENDOR_API_URL", "https://api.supplier.com/v1")
VENDOR_API_TOKEN = os.getenv("VENDOR_API_TOKEN") # Required for authentication
REQUEST_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

logger = logging.getLogger("VendorClient")

class VendorApiClient:
    """
    Client for interacting with external supplier APIs.
    Includes automatic retry logic for network failures.
    """

    def __init__(self):
        if not VENDOR_API_TOKEN:
            logger.warning("VENDOR_API_TOKEN not set. API calls may fail.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {VENDOR_API_TOKEN}",
            "User-Agent": "OrderProcessor/1.0"
        })

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def check_availability(self, sku: str) -> bool:
        """
        Checks if a product is available at the supplier.
        Retries 3 times if the connection fails.
        
        Args:
            sku (str): The product Stock Keeping Unit.
        """
        url = f"{VENDOR_API_URL}/products/{sku}/availability"
        logger.info(f"Checking stock for {sku}...")
        
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return data.get("in_stock", False)
        except requests.RequestException as e:
            logger.error(f"API Request failed: {e}")
            raise

if __name__ == "__main__":
