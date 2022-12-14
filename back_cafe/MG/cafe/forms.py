from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from cafe.models import Users
import re


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=25,
                                                                              message='Firstname must be in range 3, 25')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=25,
                                                                            message='Lastname must be in range 3, 25')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone',
                               validators=[DataRequired(), Length(min=11, max=13, message='Wrong Phone number')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password',
                                 validators=[DataRequired(),
                                             EqualTo('password', message='Confirm password must be equal to Password')])

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This Email is already exist.")

    def validate_phone_number(self, phone_number):
        if not re.match(r'^(\+989|09)+\d{9}$', phone_number.data):
            raise ValidationError("Invalid Phone number.")
        elif Users.query.filter_by(phone_number=phone_number.data).first():
            raise ValidationError("This Phone number is already exist.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')


class UpdateProfileForm(FlaskForm):
    first_name = StringField('first name', validators=[DataRequired(), Length(min=3, max=30)])
    last_name = StringField('last name ', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('email', validators=[DataRequired(), Email()])
    phone_number = StringField('phone', validators=[DataRequired(), Length(min=11, max=11)])
