import schedule
import time
import logging
from flask import current_app

# def update_daily():
#     schedule.every().day.at("00:00").do(add_currency_data)

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

def update_every_second(app):
    with app.app_context():  # Utilisez app.app_context() pour accéder au contexte de l'application Flask
        from database.requests import add_currency_data  # Importez add_currency_data à l'intérieur de la fonction
        add_currency_data()

def run_scheduler(app):  # Acceptez l'instance de l'application Flask comme argument
    # Planifiez la mise à jour des données chaque seconde
    schedule.every(15).seconds.do(update_every_second, app)

    while True:
        schedule.run_pending()
        time.sleep(1)

