import os
import requests

# Get env variable
EXCHANGE_URL = os.getenv("EXCHANGE_URL")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

def get_currency_codes():
    """Get currency codes from exchangerate API."""
    response = requests.get(f'{EXCHANGE_URL}/{EXCHANGE_API_KEY}/codes')
    data = response.json()
    return data
