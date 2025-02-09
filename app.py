from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Resume
from utils.s3_helper import upload_to_s3
from utils.ai_helper import analyze_resume, generate_interview_question, evaluate_star_response
from dotenv import load_dotenv
from flask_mail import Mail
import os
import token_utils
from token_utils import confirm_token, generate_token
from datetime import datetime
from email_sender import send_email
#from config import SECURITY_PASSWORD_SALT
#from config import SECRET_KEY
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resumes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
app.config['S3_BUCKET_NAME'] = os.getenv('S3_BUCKET_NAME')
##app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
##app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")
app.config["SECURITY_PASSWORD_SALT"]= os.getenv('SECURITY_PASSWORD_SALT')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')

app.debug = True

# Initialize database & Flask extensions
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
mail = Mail(app) #Initialize Flask-Mail
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login if user isn't authenticated
    
@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return print({'error': 'Invalid user ID'}), 400
    if(user_id):
        return db.session.get(User, int(user_id))
    else:
        return 0

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
    return render_template('dashboard.html', resumes=resumes)

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze_resume_route():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        resume_file = request.files['resume']
        job_desc = request.form.get('job_description', '')

        if resume_file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        try:
            # Read file content
            if resume_file.filename.endswith('.docx'):
                from docx import Document
                doc = Document(resume_file)
                resume_text = '\n'.join([para.text for para in doc.paragraphs])
            else:
                resume_text = resume_file.read().decode('utf-8')
            
            # Upload to S3
            s3_path = upload_to_s3(resume_file, current_user.id)
            
            # AI Analysis
            analysis = analyze_resume(resume_text, job_desc)
            
            # Save to database
            new_resume = Resume(
                user_id=current_user.id,
                s3_path=s3_path,
                analysis=analysis,
                created_at=datetime.utcnow()
            )
            db.session.add(new_resume)
            db.session.commit()
            
            return render_template('resume/analysis.html', analysis=analysis)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('analyze_resume_route'))
    
    return render_template('resume/analyze.html')

@app.route('/interview', methods=['GET', 'POST'])
@login_required
def interview():
    if request.method == 'POST':
        answer = request.form.get('answer', '')
        if not answer:
            flash('Please provide an answer', 'error')
            return redirect(url_for('interview'))
            
        try:
            evaluation = evaluate_star_response(answer)
            return render_template('evaluation.html', evaluation=evaluation)
        except Exception as e:
            flash(f'Evaluation error: {str(e)}', 'error')
            return redirect(url_for('interview'))
    
    try:
        question = generate_interview_question("Technology", "Mid-Level")
    except Exception as e:
        question = f"Error generating question: {str(e)}"
        flash(question, 'error')
    
    return render_template('interview/interview.html', question=question)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html')

@app.route('/inactive')
def inactive():
    return render_template('auth/inactive.html')  # Ensure correct path within 'templates/'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        token = generate_token(new_user.email)
        print("token success")
        confirm_url = url_for("home", token=token, _external=True)
        print("confirm_url success")
        html = render_template("auth/confirm.html", confirm_url=confirm_url)
        print("html success")
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)
        print("email success")
        login_user(new_user)

        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for('inactive'))
        
        ##flash('Registration successful! Please login', 'success')
        return render_template('auth/confirm.html')
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=False)
