import numpy as np
from models import db
from models import CurrencyConversion
# Fonction pour calculer les statistiques sur les montants convertis pour une devise spécifique
def calculate_statistics_for_currency(currency_code):
    # Récupérer les montants convertis pour la devise spécifiée depuis la base de données
    conversion_results = CurrencyConversion.query.filter_by(target_code=currency_code).all()
    
    # Extraire les montants convertis
    converted_amounts = [conversion.conversion_result for conversion in conversion_results]
    
    # Utiliser numpy pour calculer les statistiques
    if converted_amounts:
        mean = np.mean(converted_amounts)
        std_dev = np.std(converted_amounts)
        maximum = np.max(converted_amounts)
        minimum = np.min(converted_amounts)
        return {
            "currency_code": currency_code,
            "mean": mean,
            "standard_deviation": std_dev,
            "maximum": maximum,
            "minimum": minimum
        }
    else:
        return None

# Exemple d'utilisation : Calculer les statistiques pour la devise XOF


# Fonction pour comparer les statistiques des différentes devises
def compare_statistics_for_currencies():
    # Récupérer la liste des devises disponibles dans la base de données
    currency_codes = db.session.query(CurrencyConversion.target_code).distinct().all()
    currency_codes = [code[0] for code in currency_codes]
    
    # Initialiser un dictionnaire pour stocker les statistiques de chaque devise
    currency_statistics = {}
    
    # Calculer les statistiques pour chaque devise
    for currency_code in currency_codes:
        stats = calculate_statistics_for_currency(currency_code)
        if stats:
            currency_statistics[currency_code] = stats
    
    return currency_statistics

# Fonction pour calculer les moyennes des montants convertis pour chaque devise sur l'ensemble des données disponibles
def calculate_average_conversion_amounts_by_currency():
    currency_averages = {}
    trend_messages = {}
    
    # Récupérer la liste des devises disponibles dans la base de données
    currency_codes = db.session.query(CurrencyConversion.target_code).distinct().all()
    currency_codes = [code[0] for code in currency_codes]
    
    for currency_code in currency_codes:
        # Récupérer les montants convertis pour la devise spécifiée
        conversion_results = CurrencyConversion.query.filter_by(target_code=currency_code).all()
        
        # Extraire les montants convertis
        converted_amounts = [conversion.conversion_result for conversion in conversion_results]
        
        # Calculer la moyenne des montants convertis
        if converted_amounts:
            average = np.mean(converted_amounts)
            currency_averages[currency_code] = average
            
            # Déterminer la tendance
            if len(converted_amounts) >= 2:
                if converted_amounts[-1] > converted_amounts[-2]:
                    trend_messages[currency_code] = "Hausse"
                elif converted_amounts[-1] < converted_amounts[-2]:
                    trend_messages[currency_code] = "Baisse"
                else:
                    trend_messages[currency_code] = "Stable"
            else:
                trend_messages[currency_code] = "N/A"
    
    return currency_averages, trend_messages

