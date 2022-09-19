from cafe import app, bcrypt, db
from flask import render_template, flash, redirect, url_for
from cafe.forms import SignupForm
from cafe.models import Users


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email=form.email.data,
                     phone_number=form.phone.data,
                     password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash("You signed up successfully", "success")
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')
