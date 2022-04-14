import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db
from flaskDemo.forms import RegistrationForm, LoginForm
#from flaskDemo.models import User, Post,Department, Dependent, Dept_Locations, Employee, Project, Works_On
from flask_login import login_user, current_user, logout_user, login_required
from flaskDemo.models import Product, Publisher, User
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    productsTable = Product.query.all()
    return render_template('home.html', title="Home", products=productsTable)

@app.route("/books")
def books():
    productsTable = Product.query.all()
    return render_template('books_list.html', products=productsTable)

@app.route("/books/<pid>")
def book_page(pid):
    book = Product.query.filter_by(ProductID=pid).first()
    publisher = Publisher.query.filter_by(PublisherID=book.PublisherID).first()
    return render_template('books.html',title=str(book.Title),book=book, publisher=publisher)




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))