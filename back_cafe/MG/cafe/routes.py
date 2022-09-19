from cafe import app
from flask import render_template


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')
