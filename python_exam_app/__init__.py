from flask import Flask 

from flask_bcrypt import Bcrypt 

app = Flask(__name__)

app.secret_key = "Pizza Time"

DATABASE = "bands_db_blackbelt"

BCRYPT = Bcrypt(app)