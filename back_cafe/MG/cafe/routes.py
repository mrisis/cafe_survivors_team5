from flask import render_template, flash, redirect, url_for, request, jsonify, make_response, Response, session
from flask_login import login_user, current_user, login_required, logout_user

from cafe import app, bcrypt, db
from cafe.forms import SignupForm, LoginForm, UpdateProfileForm
from cafe.models import Users, Menuitems, Orders, Tables, Receipts


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


@app.route('/order', methods=['POST', 'GET'])
@login_required
def order():
    if request.method == 'GET':
        total_price = 0
        total_price_without_discount = 0
        counter = 0
        orders = []
        table = session['table']
        table = Tables.query.filter_by(id=table).first()
        print(table)
        for k, v in session.items():
            print(k, v)
            item = Menuitems.query.filter_by(name=k).first()
            if item:
                counter += 1
                total_price += ((item.price * (100 - item.discount)) / 100) * int(v)
                total_price_without_discount += item.price * int(v)
                orders.append(
                    Orders(table=table, number=int(v), status=False, user=current_user, menuitem=item, receipts=1))
        final_discount = total_price_without_discount - total_price
        return render_template('order.html', orders=orders,
                               total_price=total_price,
                               counter=counter, table=table, final_discount=final_discount)


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    menu_items = Menuitems.query.all()
    tables = Tables.query.all()
    list_of_category = list(set([item.category for item in menu_items]))

    req = session.items()
    items = []
    count = []
    for k, v in req:
        item = Menuitems.query.filter_by(name=k).first()
        if item:
            items.append(item)
            count.append(v)
    pack = zip(items, count)
    return render_template('menu.html', tables=tables, menu_items=menu_items, list_of_category=list_of_category,
                           pack=pack)


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

        receipt = Receipts(total_price=100, final_price=200, users=current_user.id)
        req = session.items()
        lst = []
        table_id = session["table"]
        tables = Tables.query.get(table_id)
        tables.use = True
        db.session.commit()
        for k, v in req:
            item = Menuitems.query.filter_by(name=k).first()
            if item:
                order = Orders(table=tables, number=int(v), status=True, user=current_user, menuitem=item,
                               receipt=receipt)
                db.session.add(order)
                db.session.commit()
                lst.append(k)

        d = {}
        for i in lst:
            session.pop(i)
        for i in Receipts.query.filter_by(user=current_user):
            d[i.id] = []
            for j in Orders.query.filter_by(user=current_user):
                if i.id == j.receipts:
                    d[i.id].append(j)

    return render_template("profile.html", form=form, orders=d)


@app.route('/session/set', methods=['GET', 'POST'])
@login_required
def set_session():
    response = request.get_json()
    for k, v in response.items():
        print(k, v)
        session[k.replace('_', ' ')] = v
    return response


@app.route('/session/delete', methods=['GET', 'POST'])
@login_required
def del_session():
    response = request.get_data().decode('utf-8')
    session.pop(response.replace('_', ' '))
    return response


@app.route('/session/down', methods=['GET', 'POST'])
@login_required
def down_session():
    response = request.get_data().decode('utf-8')
    print(response)
    session[response.replace('_', ' ')] = str(int(session[response.replace('_', ' ')]) - 1)
    return response


@app.route('/session/up', methods=['GET', 'POST'])
@login_required
def up_session():
    response = request.get_data().decode('utf-8')
    print(response)
    session[response.replace('_', ' ')] = str(int(session[response.replace('_', ' ')]) + 1)
    return response
