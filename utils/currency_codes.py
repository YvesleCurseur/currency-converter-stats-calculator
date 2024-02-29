# utils/currency_codes.py

import os
import requests

from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
# https://v6.exchangerate-api.com/v6/YOUR-API-KEY/codes

def get_currency_codes():
    """Get currency codes from exchangerate API."""

    response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/codes')
    data = response.json()
    return data
    