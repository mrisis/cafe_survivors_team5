from cafe import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from cafe.forms import SignupForm, LoginForm, UpdateProfileForm
from cafe.models import Users, Menuitems, Orders
from flask_login import login_user, current_user, login_required, logout_user


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
                     phone_number=form.phone_number.data,
                     password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash("You signed up successfully", "success")
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You logged in successfully", "success")
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you logged out account", 'danger')
    return redirect(url_for('home'))


@app.route('/order')
def order():
    orders = Orders.query.filter_by(user=current_user)
    total_price = 0
    counter = 0
    for order in orders:
        counter += 1
        total_price += order.menuitem.price - order.menuitem.discount
    return render_template('order.html', orders=orders, total_price=total_price, counter=counter)


@app.route('/menu')
def menu():
    menu_items = Menuitems.query.all()
    list_of_category = list(set([item.category for item in menu_items]))
    return render_template('menu.html', menu_items=menu_items, list_of_category=list_of_category)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    orders = Orders.query.filter_by(user=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('updated your profile ', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.last_name.data = current_user.last_name
    return render_template("profile.html", form=form, orders=orders)
