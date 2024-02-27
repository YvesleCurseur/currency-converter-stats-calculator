import os

# flask import
from flask import Flask, render_template, request

# env config
from dotenv import load_dotenv

import requests

app = Flask(__name__)

# Loading env variables
load_dotenv()

RAPIDAPI_CURRENCY_CONVERT_URL = os.getenv("RAPIDAPI_CURRENCY_CONVERT_URL")
RAPIDAPI_CURRENCY_CONVERT_HOST = os.getenv("RAPIDAPI_CURRENCY_CONVERT_HOST")
RAPIDAPI_CURRENCY_CONVERT_API_KEY = os.getenv("RAPIDAPI_CURRENCY_CONVERT_API_KEY")

print(RAPIDAPI_CURRENCY_CONVERT_URL)


# ===============================================================
# | Homme Page
# ===============================================================
@app.route("/")
def index():
    return render_template("convert.html")


# Route pour gérer la conversion de devises
@app.route("/convert", methods=["POST"])
def convert():
    amount_str = request.form.get("amount")
    if not amount_str:
        return (
            "Veuillez saisir un montant valide.",
            400,
        )  # Retourne une réponse d'erreur 400 Bad Request si le montant est vide

    try:
        amount = float(amount_str)
    except ValueError:
        return (
            "Le montant saisi n'est pas valide.",
            400,
        )  # Retourne une réponse d'erreur 400 Bad Request si le montant ne peut pas être converti en flottant

    to_currency = request.form.get("to_currency")
    from_currency = request.form.get("from_currency")

    querystring = {"from_amount": amount, "from": from_currency, "to": to_currency}

    headers = {
        "x-rapidapi-host": RAPIDAPI_CURRENCY_CONVERT_HOST,
        "x-rapidapi-key": RAPIDAPI_CURRENCY_CONVERT_API_KEY,
    }

    response = requests.get(
        url=RAPIDAPI_CURRENCY_CONVERT_URL,
        headers=headers,
        params=querystring,
    )
    result = response.json()
    print(result)

    return render_template("convert.html", result=result)
