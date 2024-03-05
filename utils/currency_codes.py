import os
import requests

# Import and loading env variable

# Delete
# from dotenv import load_dotenv
# load_dotenv()
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

def get_currency_codes():
    """Get currency codes from exchangerate API."""
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/codes')
    data = response.json()
    return data
