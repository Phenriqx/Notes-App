from flask import render_template, redirect, url_for, flash
from flask_login import login_manager, current_user, login_user, logout_user
from website import db, app
from website.forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title='Log in')

@app.route('/logout')
def logout():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register')