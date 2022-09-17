from cafe import db
import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship("Orders", backref="author",lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.first_name}, {self.last_name})'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.Integer, db.ForeignKey(), nullable=False)
    menu_items = db.Column(db.ForeignKey(""), unique=True, nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

 def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.menu_items}, {self.status})'
