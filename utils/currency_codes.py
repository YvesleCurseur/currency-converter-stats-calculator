# utils/currency_codes.py

import os
import requests
import numpy as np

from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
# https://v6.exchangerate-api.com/v6/YOUR-API-KEY/codes

def get_currency_codes():
    """Get currency codes from exchangerate API."""
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/codes')
    data = response.json()
    return data


def statistical_calculations(amount_converted):
    average = np.mean(amount_converted)
    standard_deviation = np.std(amount_converted)
    maximum = np.max(amount_converted)
    minimum = np.min(amount_converted)

    return average, standard_deviation, maximum, minimum