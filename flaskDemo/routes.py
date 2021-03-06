import mysql.connector
from mysql.connector import Error
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
from sqlalchemy import func

 
cartlist = list()
titlelist = []

def connect(sql):
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='books',
                                       user='student',
                                       password='student')
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
        else:
            return('problem')
        cursor.execute(sql)
        rows = cursor.fetchall()   
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()

    return rows

@app.route("/")
@app.route("/home")
def home():
   
    """ Connect to MySQL database """
    """ Report -- #8 """
    rows = connect("SELECT * FROM Product")
    """ Report -- #10 """
    bookchoice = connect("SELECT count(*) AS sum FROM Product")
    productsTable = Product.query.all()
    isbns = Book.query.all()
    return render_template('home.html', title="Home", products=productsTable, isbns=isbns, booktitle = rows, books = bookchoice )

@app.route("/books")
def books():
    productsTable = Product.query.all()
    return render_template('books_list.html', products=productsTable)

@app.route("/books/<pid>")
def book_page(pid):
    book = Product.query.filter_by(ProductID=pid).first()
    isbn = Book.query.filter_by(ProductID=pid).first()
    publisher = Publisher.query.filter_by(PublisherID=book.PublisherID).first()
    print("Book:", book)
    print("Book Type: ", book.Type)
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
    customer = Customer.query.filter(Customer.Email==current_user.email).first()
 
    order = Orders(CustomerID = customer.CustomerID, DateOfOrder = datetime.today().strftime("%Y-%m-%d"), UserEmail = current_user.email)
    db.session.add(order)
    db.session.commit()
    lastinOrder = Orders.query.order_by(Orders.OrderID.desc()).first()
    for item in titlelist:
        
        book = Product.query.filter_by(Title=item).first()
        orderline= Orderline(OrderID = lastinOrder.OrderID, ProductID = book.ProductID , Quantity = 1)
        
        db.session.add(orderline)
        db.session.commit()
       
    lastinOrderLine = Orderline.query.order_by(Orderline.OrderID.desc()).first()
    customerEmail = current_user.email
    customerID = Customer.query.filter_by(Email=customerEmail).first()
    cartlist.clear()
    titlelist.clear()
    return render_template('homeaftercheckout.html', title="Home")

"""#14 User Form"""
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
#    last = Customer.query.order_by(Customer.CustomerID.desc()).first()
#    lastCustomer = last.CustomerID + 1 
  
    
    if form.validate_on_submit():
        last = Customer.query.order_by(Customer.CustomerID.desc()).first()
        lastCustomer = last.CustomerID + 1 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        customer = Customer(CustomerID = lastCustomer, CustomerFirstName=form.firstName.data, CustomerLastName=form.lastName.data,
        Address=form.address.data, City=form.city.data, State=form.state.data, Zip=form.zip.data, Email=form.email.data)
        db.session.add_all([user,customer])
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


@app.route("/adminpage", methods=['GET', 'POST'])
def adminpage():
    """ Report #11 & #12 Regular SQL"""
    mostPopularBooks = connect("SELECT Product.Title, Product.RetailPrice, Product.ProductID, Count(Orderline.ProductID) as numSold, Category\
        FROM `product`, orderline\
        where Product.ProductID = orderline.ProductID and Type = 'b'\
        group by ProductID\
        order by numSold desc\
        limit 3;")
    """ Report # 9 & 11 & 12 SQLAlchemy"""
    mostPopularSubscriptions = db.session.query(Product.Title, Product.RetailPrice, Product.Category, func.count(Orderline.ProductID).label('count'))\
    .select_from(Product).join(Orderline).filter(Product.Type == 's', Product.ProductID == Orderline.ProductID).group_by(Product.ProductID).order_by(func.count(Orderline.ProductID).desc()).limit(3).all()

    """ Report #13 Regular SQL"""
    customersNotOrdered = connect("SELECT CustomerID, CustomerFirstName, CustomerLastName, Email FROM `customer` where CustomerID not in (Select customer.CustomerID from customer, orders where customer.CustomerID = orders.CustomerID);")
    

    subquery1 = db.session.query(Customer.CustomerID).join(Orders,Customer.CustomerID==Orders.CustomerID).join(Orderline, Orderline.OrderID==Orders.OrderID)\
    .join(Product, Product.ProductID==Orderline.ProductID).filter(Product.Type=='s').distinct()
    
    booksandsubs = db.session.query(Customer.CustomerFirstName, Customer.CustomerLastName, Customer.Email, func.sum(Product.RetailPrice).label('Money'))\
    .join(Orders,Customer.CustomerID==Orders.CustomerID)\
    .join(Orderline, Orderline.OrderID==Orders.OrderID)\
    .join(Product, Product.ProductID==Orderline.ProductID).filter(Product.Type=='b', Customer.CustomerID.in_(subquery1)).distinct()
   
    
    return render_template('adminpage.html', books=mostPopularBooks, subscriptions=mostPopularSubscriptions, customers = customersNotOrdered, emails = booksandsubs, )

@app.route("/delete_book/<pid>", methods=['GET', 'POST'])
def delete_book(pid):
    product = Product.query.get_or_404(pid)
    book = Book.query.get_or_404(pid)

    db.session.delete(book)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('home'))

"""Report #6, #14, #15"""
@app.route("/update/<pid>", methods=['GET', 'POST'])
def update(pid):
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

    return render_template('update.html', form=form)