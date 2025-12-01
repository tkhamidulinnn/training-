import os
import requests  # INSTALLATION: pip install requests

# ==========================================
# 💱 FOREX CONFIGURATION
# ==========================================
# Settings for the Currency Conversion Service
# ==========================================
FOREX_API_KEY = os.getenv("FOREX_API_KEY")  # Required: API Key from provider
FOREX_BASE_URL = os.getenv("FOREX_URL", "https://api.exchangerate-api.com/v4/latest/")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")

class CurrencyConverter:
    """
    Handles real-time currency conversion operations.
    """
    
    def __init__(self):
        if not FOREX_API_KEY:
            print("Warning: FOREX_API_KEY is not set. Rate limits may apply.")

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Fetches the current exchange rate.
        
        Args:
            from_currency (str): Source currency code (e.g. 'USD')
            to_currency (str): Target currency code (e.g. 'EUR')
        """
        url = f"{FOREX_BASE_URL}{from_currency}"
        response = requests.get(url)
        data = response.json()
        return data["rates"][to_currency]

    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        """Calculates the converted amount."""
        rate = self.get_rate(from_curr, to_curr)
        return amount * rate

if __name__ == "__main__":
    # Usage Example
    converter = CurrencyConverter()
    print(f"100 USD in EUR: {converter.convert(100, 'USD', 'EUR')}")
