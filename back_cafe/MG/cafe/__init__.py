from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = "49f4d03ee119ec59346acb4c953a4220"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../cafe.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please login'
from cafe.models import *
admin = Admin(app)

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Menuitems, db.session))
admin.add_view(ModelView(Orders, db.session))
admin.add_view(ModelView(Tables, db.session))
admin.add_view(ModelView(Receipts, db.session))

from cafe import routes
