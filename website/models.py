from website import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    notes = db.relationship('Notes', backref='author', lazy=True)
    
    def __repr__(self):
        return f'User (username: {self.username}, email: {self.email})'
    
    def __str__(self):
       return f'Username: {self.username}, Email: {self.email}'
    
    
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.relationship('Categories', backref='category', lazy=True)
    
    def __repr__(self):
        return f'title: {self.title} at {self.date_posted}'
    
    def __str__(self):
        return f'title: {self.title} by {self.author}'
    
    
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    
    def __repr__(self):
        return f'Category: {self.name}'
    

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()