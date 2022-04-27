import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import BookPriceUpdateForm, RegistrationForm, LoginForm
#from flaskDemo.models import User, Post,Department, Dependent, Dept_Locations, Employee, Project, Works_On
from flask_login import login_user, current_user, logout_user, login_required
from flaskDemo.models import Customer, Orderline, Product, Publisher, User, Orders, Orderline, Book
from datetime import datetime


cartlist = list()
titlelist = []

@app.route("/")
@app.route("/home")
def home():
    productsTable = Product.query.all()
    isbns = Book.query.all()
    return render_template('home.html', title="Home", products=productsTable, isbns=isbns)

@app.route("/books")
def books():
    productsTable = Product.query.all()
    return render_template('books_list.html', products=productsTable)

@app.route("/books/<pid>")
def book_page(pid):
    book = Product.query.filter_by(ProductID=pid).first()
    isbn = Book.query.filter_by(ProductID=pid).first()
    publisher = Publisher.query.filter_by(PublisherID=book.PublisherID).first()
    return render_template('books.html',title=str(book.Title),book=book, publisher=publisher, isbn=isbn)

@app.route("/addbook/<book>")
def add_book(book):
    cartdictionary = dict()
    cartdictionary ['pid'] = book
    cartlist.append (cartdictionary)
    print (cartlist)
    shopping_cart
    flash('Book added to cart!','success')
    productsTable = Product.query.all()
    # sends user to shopping cart after adding item
    return redirect(url_for('shopping_cart'))

@app.route("/homeaftercart")
def homeaftercart():
    return render_template('homeaftercart.html', title="Home")

@app.route("/orders")
def orders():
    orders = Orders.query.join(Orderline, Orders.OrderID == Orderline.OrderID)\
        .add_columns(Orders.OrderID, Orders.DateOfOrder, Orders.ShippingDate, Orderline.Quantity, Orders.UserEmail)\
        .join(Product, Orderline.ProductID == Product.ProductID)\
        .add_columns(Product.Title, Product.Category, Product.RetailPrice)\
        .join(Publisher, Product.PublisherID == Publisher.PublisherID)\
        .add_columns(Publisher.Name)\
        .join(Customer, Orders.CustomerID == Customer.CustomerID)\
        .add_columns(Customer.CustomerFirstName, Customer.CustomerLastName)\
        .order_by(Orders.OrderID)
    return render_template('orders.html', orders=orders)

@app.route("/shoppingcart")
def shopping_cart():
    for item in cartlist:
        cart = Product.query.filter_by(ProductID=item['pid']).first()
        if cart.Title not in titlelist:
            titlelist.append(cart.Title) 

    print (titlelist)
    return render_template('shoppingcart.html', title="shoppingcart", titlelist=titlelist )

@app.route("/checkout")
def checkout():
    # have to add .first() to make it work
    last = Orderline.query.order_by(Orderline.OrderID.desc()).first()
    last.OrderID = last.OrderID + 1
    for item in titlelist:
        book = Product.query.filter_by(Title=item).first()
        orderline= Orderline(OrderID = last.OrderID, ProductID = book.ProductID , Quantity = 1) 
        # --- print for debugging ---
        print("Adding to Orderline: %d, %d, %d" % (last.OrderID, book.ProductID, 1))
        print("cartlist:")
        print(cartlist)
        print("titlelist:")
        print( titlelist)
        db.session.add(orderline)
        db.session.commit()
    lastinOrderLine = Orderline.query.order_by(Orderline.OrderID.desc()).first()
    customerEmail = current_user.email
    customerID = Customer.query.filter_by(Email=customerEmail).first()
    order = Orders(OrderID = lastinOrderLine.OrderID, CustomerID = customerID.CustomerID, DateOfOrder = datetime.today().strftime("%Y-%m-%d"), UserEmail = current_user.email)
    db.session.add(order)
    db.session.commit()
    cartlist.clear()
    titlelist.clear()
    return render_template('homeaftercheckout.html', title="Home")


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


@app.route("/adminpage/<pid>", methods=['GET', 'POST'])
def adminpage(pid):
    #product = Product.query.get_or_404(pid)

    form = BookPriceUpdateForm()

    if form.validate_on_submit:
        print("button pressed")
        #pt = form.productTitle.data
        #pt = "Patriot Games"
        product = Product.query.get(pid)
        newPrice = form.newPrice.data
        product.RetailPrice = newPrice
        db.session.commit()
        print(newPrice)
        print(product)
        print(product.RetailPrice)


    

    return render_template('adminpage.html', form=form)

@app.route("/delete_book/<pid>", methods=['GET', 'POST'])
def delete_book(pid):
    product = Product.query.get_or_404(pid)
    book = Book.query.get_or_404(pid)

    db.session.delete(book)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('home'))