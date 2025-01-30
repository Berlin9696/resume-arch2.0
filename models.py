from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Import UserMixin

# Define Base for SQLAlchemy
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):  # Add UserMixin to support Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    resumes = db.relationship('Resume', backref='user', lazy=True)

    # Flask-Login required attributes
    @property
    def is_active(self):  # Needed for account activation
        return True

    @property
    def is_authenticated(self):  # Indicates if user is logged in
        return True

    @property
    def is_anonymous(self):  # False since users must authenticate
        return False

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    s3_path = db.Column(db.String(255), nullable=False)
    analysis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
