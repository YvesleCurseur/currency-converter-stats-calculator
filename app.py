import os

# flask import
from flask import render_template, request
from config import app

# env config
from dotenv import load_dotenv

load_dotenv()

# db import
from models import (
    list_currency_codes, 
    add_currency_conversion_data, 
    list_currency_conversions)
from utils.statistics import (
    calculate_statistics_for_currency, 
    compare_statistics_for_currencies, 
    calculate_average_conversion_amounts_by_currency)

import requests

# Loading env variables
EXCHANGE_URL = os.getenv("EXCHANGE_URL")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


# ===============================================================
# | Homme Page
# ===============================================================
@app.route("/")
def index():
    codes = list_currency_codes()
    print(codes)
    return render_template("base.html", codes=codes)

@app.route("/convert", methods=["GET"])
def show_convert_form():
    codes = list_currency_codes()
    return render_template("convert.html", codes=codes)

@app.route("/conversions", methods=["GET"])
def convertions():
    conversions = list_currency_conversions()
    return render_template("conversions.html", conversions=conversions)

# Route pour gérer la conversion de devises
@app.route("/convert", methods=["GET", "POST"])
def convert():
    # RECUPERATION DES DONNEES
    codes = None
    codes = list_currency_codes()

    amount_str = request.form.get("amount")
    if not amount_str:
        return (
            "Veuillez saisir un montant valide.",
            400,
        )  # Retourne une réponse d'erreur 400 Bad Request si le montant est vide

    try:
        # AMOUNT variable (decimal format xxxx.xxxx).
        amount = float(amount_str)
    except ValueError:
        return (
            "Le montant saisi n'est pas valide.",
            400,
        )  # Retourne une réponse d'erreur 400 Bad Request si le montant ne peut pas être converti en flottant

    to_currency = request.form.get("to_currency")
    from_currency = request.form.get("from_currency")

    response = requests.get(
        f"{EXCHANGE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    )

    if response.status_code != 200:
        return (
            "Une erreur s'est produite lors de la conversion. Veuillez réessayer.",
            response.status_code,  # Include the status code
        )

    result = response.json()

    # Add from_amount in the result json
    result["from_amount"] = amount

    add_currency_conversion_data(data=result)

    return render_template("convert.html", result=result, codes=codes)


# Route pour les statistiques
@app.route("/statistics", methods=["POST", "GET"])
def statistics():

    currency_code = request.form.get("currency_code")
    conversions = list_currency_conversions()
    stats = calculate_statistics_for_currency(currency_code)

    return render_template("statistics.html", stats=stats, conversions=conversions)


@app.route("/trends", methods=["GET"])
def trends():

    # Exemple d'utilisation : Comparer les statistiques des différentes devises
    currency_comparison_stats = compare_statistics_for_currencies()
    print("Currency Comparison Statistics:", currency_comparison_stats)

    # Exemple d'utilisation : Calculer les moyennes des montants convertis et les tendances pour chaque devise sur l'ensemble des données disponibles
    average_conversion_amounts, trend_messages = calculate_average_conversion_amounts_by_currency()

    # Affichage des moyennes des montants convertis pour chaque devise
    print("Average Conversion Amounts:", average_conversion_amounts)

    # Affichage des tendances des montants convertis pour chaque devise
    print("Trend Messages:")
    for currency_code, trend in trend_messages.items():
        print(f"- {currency_code} : {trend}")

    return render_template("trends.html", trends=trend_messages, currency_comparison_stats=currency_comparison_stats, average_conversion_amounts=average_conversion_amounts)


# Statistics for XOF: {'currency_code': 'XOF', 'mean': 363606.78, 'standard_deviation': 363421.62, 'maximum': 727028.4, 'minimum': 185.16}   
# Currency Comparison Statistics: {'XOF': {'currency_code': 'XOF', 'mean': 363606.78, 'standard_deviation': 363421.62, 'maximum': 727028.4, 'minimum': 185.16}}