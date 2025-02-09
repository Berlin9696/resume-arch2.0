from flask_mail import Message

import app
import os
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@flask.com')

mail = Mail(app)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.getenv('MAIL_DEFAULT_SENDER'),
    )
    print(app.config['MAIL_PASSWORD'])
    print(app.config['MAIL_SERVER'])
    try:
        with app.app_context():
            mail.send(msg)
        print(f"Email sent successfully to {to}")
    except Exception as e:
        print(f"Email sending failed: {e}")
