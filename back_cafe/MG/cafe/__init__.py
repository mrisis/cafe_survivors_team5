from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "49f4d03ee119ec59346acb4c953a4220"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../cafe.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from cafe import routes
