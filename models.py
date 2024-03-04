import os
from config import app
from flask_sqlalchemy import SQLAlchemy
from utils.currency_codes import get_currency_codes

db = SQLAlchemy()

db.init_app(app)  # Initialisez db après avoir créé l'application Flask

class Currency(db.Model):
    __tablename__ = "currencies"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.code} - {self.name}"


def add_currency_data():
    currency_data = get_currency_codes()
    for code, name in currency_data["supported_codes"]:
        currency = Currency.query.filter_by(code=code).first()
        if not currency:
            currency = Currency(code=code, name=name)  # Create a new currency
            db.session.add(currency)
    db.session.commit()


def get_currency_name(code):
    currency = Currency.query.filter_by(code=code).first()
    if currency:
        return currency.name
    else:
        return "Currency not found"


def list_currency_codes():
    code = Currency.query.order_by(Currency.id).all()
    return code

class CurrencyConversion(db.Model):
    __tablename__ = "currency_conversions"
    id = db.Column(db.Integer, primary_key=True)
    from_amount = db.Column(db.Float, nullable=False)
    base_code = db.Column(db.String(3), nullable=False)
    target_code = db.Column(db.String(3), nullable=False)
    conversion_rate = db.Column(db.Float, nullable=False)
    conversion_result = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<CurrencyConversion {self.base_code} to {self.target_code}>"

def add_currency_conversion_data(data):
    currency_conversion = CurrencyConversion(
        base_code=data["base_code"],
        target_code=data["target_code"],
        from_amount=data["from_amount"],
        conversion_rate=data["conversion_rate"],
        conversion_result=data["conversion_result"]
    )
    db.session.add(currency_conversion)
    db.session.commit()

# List all the conversions
def list_currency_conversions():
    conversions = CurrencyConversion.query.order_by(CurrencyConversion.id).all()
    print(conversions)
    return conversions

with app.app_context():
    if not os.path.exists("currency_data.db"):
        db.create_all()
        add_currency_data()