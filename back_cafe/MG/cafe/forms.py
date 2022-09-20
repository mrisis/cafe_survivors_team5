from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from cafe.models import Users


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=25,
                                                                              message='Firstname must be in range 3, 25')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=25,
                                                                            message='Lastname must be in range 3, 25')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11, message='Wrong Phone number')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password',
                                 validators=[DataRequired(),
                                             EqualTo('password', message='Confirm password must be equal to Password')])

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This Email is already exist.")

    def validate_phone_number(self, phone_number):
        user = Users.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError("This Phone number is already exist.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')


