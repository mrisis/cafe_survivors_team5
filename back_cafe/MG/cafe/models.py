from cafe import db, login_manager
import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship("Orders", backref="author", lazy=True)
    tables = db.relationship("Tables", backref="author", lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.first_name}, {self.last_name})'


class Menuitems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(40))
    discount = db.Column(db.Float, nullable=True)
    serving_time_period = db.Column(db.Integer, nullable=False)
    estimated_cooking_time = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Orders', backref="author", lazy=True)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id} - {self.name} - {self.category})"


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receipts = db.relationship("Receipts", backref="author", lazy=True)
    menu_items = db.Column(db.Integer, db.ForeignKey("menuitems.id"), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.menu_items}, {self.status})'


class Tables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False, unique=True)
    cafe_space_position = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id} - {self.table_number} - {self.cafe_space_position})"


class Receipts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id} - {self.total_price} - {self.final_price} - {self.timestamp})"
