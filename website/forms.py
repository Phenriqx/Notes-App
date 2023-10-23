from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from website.models import User, Categories


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
    

class AddNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=60)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[Length(min=1, max=50)])
    submit = SubmitField('Add Note')
    
    def validate_category(self, category):
        ctg = Categories.query.filter_by(name=category.data).first()
        if not ctg:
            raise ValidationError('This category does not exist!')

class AddCategoryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Add Category')
    
    def validate_category(self, category):
        ctg = Categories.query.filter_by(name=category.data).first()
        if ctg:
            raise ValidationError('This category already exists!')