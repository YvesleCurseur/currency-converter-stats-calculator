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

class Convertion(db.Model):
    __tablename__ = "convertions"
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.String(3), nullable=False)
    to_currency = db.Column(db.String(3), nullable=False)
    

with app.app_context():
    if not os.path.exists("currency_data.db"):
        db.create_all()
        add_currency_data()