import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "currency_data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy()

db.init_app(app)  # Initialisez db après avoir créé l'application Flask

with app.app_context():
    if not os.path.exists("currency_data.db"):
        db.create_all()
