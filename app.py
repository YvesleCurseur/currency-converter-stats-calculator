import os
import requests

# flask import
from flask import render_template, request
from config import app

# db import
from models import (
    list_currency_codes,
    add_currency_conversion_data,
    list_currency_conversions,
)

# utils import
from utils.statistics import (
    calculate_statistics_for_currency,
    compare_statistics_for_currencies,
    calculate_mean_conversion_amounts_by_currency,
)


# Import env variables
EXCHANGE_URL = os.getenv("EXCHANGE_URL")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


# ===============================================================
# | Homme Page
# ===============================================================
@app.route("/")
def index():
    # Get the Home Page
    return render_template("base.html")


# ===============================================================
# | Convert Page
# ===============================================================
@app.route("/convert", methods=["GET"])
def show_convert_form():
    # Get the list of currency codes from the db
    codes = list_currency_codes()
    return render_template("convert.html", codes=codes)


# ===============================================================
# | Convert Process Page
# ===============================================================
@app.route("/convert", methods=["GET", "POST"])
def convert():
    # Get the list of currency codes from the db
    codes = list_currency_codes()
    # Get the form data
    amount_str = request.form.get("amount")
    if not amount_str:
        return (
            "The amount is empty.",
            400,
        )  # Return a 400 Bad Request error if the amount is empty
    try:
        # Amount variable (decimal format xxxx.xxxx).
        amount = float(amount_str)
    except ValueError:
        return (
            "The amount is not valid.",
            400,
        )  # Return a 400 Bad Request error if the amount is not valid
    to_currency = request.form.get("to_currency")
    from_currency = request.form.get("from_currency")
    response = requests.get(
        f"{EXCHANGE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    )
    if response.status_code != 200:
        return (
            "A server error occurred.",
            response.status_code,  # Include the status code
        )
    result = response.json()
    # Add from_amount in the result json
    result["from_amount"] = amount
    # Add the conversion result in db
    add_currency_conversion_data(data=result)
    return render_template("convert.html", result=result, codes=codes)


# ===============================================================
# | Convertions Listing Page
# ===============================================================
@app.route("/conversions", methods=["GET"])
def convertions():
    # Get the list of currency codes from the db
    conversions = list_currency_conversions()
    return render_template("conversions.html", conversions=conversions)


# ===============================================================
# | Statistics Page
# ===============================================================
@app.route("/statistics", methods=["POST", "GET"])
def statistics():
    # Get the currency code from the form
    currency_code = request.form.get("currency_code")
    # Get the list of currency codes from the db
    conversions = list_currency_conversions()
    # Get the statistics
    stats = calculate_statistics_for_currency(currency_code)
    return render_template("statistics.html", stats=stats, conversions=conversions)


# ===============================================================
# | Trends Page
# ===============================================================
@app.route("/trends", methods=["GET"])
def trends():
    # Compare statistics for currencies
    currency_comparison_stats = compare_statistics_for_currencies()
    # Calculate the mean conversion amounts for each currency
    mean_conversion_amounts, trend_messages = (
        calculate_mean_conversion_amounts_by_currency()
    )
    return render_template(
        "trends.html",
        trends=trend_messages,
        currency_comparison_stats=currency_comparison_stats,
        mean_conversion_amounts=mean_conversion_amounts,
    )
