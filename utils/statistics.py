import numpy as np
from models import db
from models import CurrencyConversion


def calculate_statistics_for_currency(currency_code):
    """Calculate the stats of all amount converted for each currency

    Args:
        currency_code (str): the currency code for the calculation

    Returns:
        dict: Dict of mean, standard_deviation, maximum, minimum and the currency
    """
    # Retreive the amounts converted for each currency specified from the db
    conversion_results = CurrencyConversion.query.filter_by(
        target_code=currency_code
    ).all()

    # Extract the amount converted
    converted_amounts = [
        conversion.conversion_result for conversion in conversion_results
    ]

    # Use numpy to calculate the stats
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
            "minimum": minimum,
        }
    else:
        return None

def compare_statistics_for_currencies():
    """Compare the statistics of all amount converted for each currency

    Returns:
        dict: Dict of currency_code, mean, standard_deviation, maximum, minimum
    """
    # Get the amounts converted for each currency specified from the db
    currency_codes = db.session.query(CurrencyConversion.target_code).distinct().all()
    currency_codes = [code[0] for code in currency_codes]

    # Init a dictionary to store the statistics of each currency
    currency_statistics = {}

    # Calculate the statistics for each currency
    for currency_code in currency_codes:
        stats = calculate_statistics_for_currency(currency_code)
        if stats:
            currency_statistics[currency_code] = stats

    return currency_statistics


def calculate_mean_conversion_amounts_by_currency():
    """Calculate the mean conversion amounts for each currency

    Returns:
        dict & str: Dict of average conversion amounts and trend messages
    """
    currency_averages = {}
    trend_messages = {}

    # Get the list of currency codes
    currency_codes = db.session.query(CurrencyConversion.target_code).distinct().all()
    currency_codes = [code[0] for code in currency_codes]

    for currency_code in currency_codes:
        # Get the amounts converted for each currency
        conversion_results = CurrencyConversion.query.filter_by(
            target_code=currency_code
        ).all()

        # Extract the amount converted
        converted_amounts = [
            conversion.conversion_result for conversion in conversion_results
        ]

        # Calculate the mean
        if converted_amounts:
            average = np.mean(converted_amounts)
            currency_averages[currency_code] = average

            # Get the trend
            if len(converted_amounts) >= 2:
                if converted_amounts[-1] > converted_amounts[-2]:
                    trend_messages[currency_code] = "Rise"
                elif converted_amounts[-1] < converted_amounts[-2]:
                    trend_messages[currency_code] = "Drop"
                else:
                    trend_messages[currency_code] = "Stable"
            else:
                trend_messages[currency_code] = "N/A"

    return currency_averages, trend_messages
