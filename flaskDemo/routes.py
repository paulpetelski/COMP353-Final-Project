import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db
#from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, DeptForm,DeptUpdateForm, AssignForm
#from flaskDemo.models import User, Post,Department, Dependent, Dept_Locations, Employee, Project, Works_On
#from flask_login import login_user, current_user, logout_user, login_required
from flaskDemo.models import Product
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    productsTable = Product.query.all()
    return render_template('home.html', products=productsTable)
