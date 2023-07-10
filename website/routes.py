from flask import render_template, redirect, url_for, flash
from flask_login import login_manager, current_user, login_user, logout_user
from website import db, app
from website.models import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/register')
def register():
    pass