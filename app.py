import os

# flask import
from flask import render_template, request
from config import app

# env config
from dotenv import load_dotenv

load_dotenv()

# db import
from models import Currency, list_currency_codes
from utils.currency_codes import statistical_calculations

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
    return render_template("convert.html", codes=codes)


# Route pour gérer la conversion de devises
@app.route("/convert", methods=["POST"])
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

    # Here is the endpoint i have to create https://v6.exchangerate-api.com/v6/9328d7790738eab570d5c8a4/pair/EUR/GBP/50

    response = requests.get(
        f"{EXCHANGE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    )

    if response.status_code != 200:
        return (
            "Une erreur s'est produite lors de la conversion. Veuillez réessayer.",
            response.status_code,  # Include the status code
        )

    result = response.json()

    # average, standard_deviation, maximum, minimum = statistical_calculations(result.result.conversion_result)

    # print(average, standard_deviation, maximum, minimum)

    results = result.get("result", {})

    # Assurez-vous que les données de conversion existent dans le résultat
    if "conversion_result" in results:
        conversion_result = float(results["conversion_result"])
        average, standard_deviation, maximum, minimum = statistical_calculations(
            conversion_result
        )
        print(average, standard_deviation, maximum, minimum)

    return render_template("convert.html", result=result, codes=codes)


@app.route("/about", methods=["GET"])
def about():
    average, standard_deviation, maximum, minimum = statistical_calculations(
        float(10.00)
    )
    print(average, standard_deviation, maximum, minimum)
    return render_template("about.html")
