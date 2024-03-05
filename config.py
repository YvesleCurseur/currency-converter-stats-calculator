import os
from flask import Flask

# Get the path of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Setup the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "currency_data.db"
)
# Disable the Flask-SQLAlchemy event system
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
