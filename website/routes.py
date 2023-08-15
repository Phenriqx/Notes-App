from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_manager, current_user, login_user, logout_user, login_required
from website import db, app, bcrypt
from website.forms import RegistrationForm, LoginForm, AddNoteForm
from website.models import User, Notes


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        notes = Notes.query.filter_by(user_id=user.id).all()
        return render_template('notes.html', notes=notes)
    return redirect(url_for('login'))


@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def add_notes():
    form = AddNoteForm()
    if form.validate_on_submit():
        note = Notes(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_notes.html', form=form, title='Add Note')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        hashed_pw = bcrypt.check_password_hash(user.password, form.password.data)
        if user and hashed_pw:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title='Log in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/note/<int:note_id>/delete>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Notes.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('index'))