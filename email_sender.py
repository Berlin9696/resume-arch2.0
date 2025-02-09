from flask_mail import Message
import os

def send_email(to, subject, template):
    # Import the app and mail objects locally to avoid circular dependencies.
    # This assumes that your main app (in app.py) has created and configured
    # the Flask app instance and initialized the Mail extension.
    from app import app, mail

    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config.get('MAIL_DEFAULT_SENDER', 'noreply@flask.com')
    )
    
    try:
        # Ensure we're in the app context when sending the email.
        with app.app_context():
            mail.send(msg)
        print(f"Email sent successfully to {to}")
    except Exception as e:
        print(f"Email sending failed: {e}")
