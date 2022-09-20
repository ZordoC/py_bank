"""Backend API."""
from flask import Flask
from api.config import Config


app = Flask(__name__)
app.config.from_object(Config)


from api import routes
