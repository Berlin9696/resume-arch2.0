from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, redirect, url_for, flash

import app
import os
app = Flask(__name__)

def generate_token(email):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
        return email
    except Exception:
        print(f"Error in confirm_token: {Exception}")
        return False
