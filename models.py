from config import db
from utils.currency_codes import get_currency_codes


class Currency(db.Model):
    __tablename__ = "currencies"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Currency Code={self.code}"


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
    return [currency.code for currency in Currency.query.order_by(Currency.id).all()]
