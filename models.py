from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# Define Base for SQLAlchemy
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):  
    __tablename__ = "users"  # Explicit table name to avoid reserved keywords
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Indexed for faster lookup
    password_hash = db.Column(db.String(255), nullable=False)  # Stores hashed password
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Ensure UTC
    
    # Relationship to Resume with Cascade Delete
    resumes = db.relationship(
        'Resume', backref='user', lazy="joined", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    __tablename__ = "resumes"  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', name="fk_resume_user_id", ondelete="CASCADE"), nullable=False, index=True
    )  # Explicit Foreign Key Name Fix
    s3_path = db.Column(db.String(255), nullable=False)  # AWS S3 link to the resume file
    region = db.Column(db.String(100), nullable=False)  # User's region
    country = db.Column(db.String(100), nullable=False)  # User's country
    analysis = db.Column(db.Text, nullable=True)  # AI-generated analysis
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # Timestamp for upload
