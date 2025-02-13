from flask_mail import Mail, Message
import os
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Load email configuration from environment variables
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))  # Ensure it's an integer
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() in ["true", "1"]
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False").lower() in ["true", "1"]
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "noreply@flask.com")

# Initialize Mail instance
mail = Mail(app)

def send_email(to, subject, template):
    """Sends an email using Flask-Mail"""
    from app import app  # Import inside function to avoid circular dependency

    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=app.config.get("MAIL_DEFAULT_SENDER", "noreply@flask.com")
    )

    try:
        with app.app_context():
            mail.send(msg)
        print(f" Email sent successfully to {to}")
    except Exception as e:
        print(f" Email sending failed: {e}")

    # Debugging - Print email settings (optional, remove in production)
    print("Debug Info:")
    print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
    print(f"MAIL_USE_SSL: {app.config['MAIL_USE_SSL']}")
    print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']} (Hidden for security)")
