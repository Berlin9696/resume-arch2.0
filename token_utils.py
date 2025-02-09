# token_utils.py (modified)
import jwt
import os

def generate_token(email):
    # Read the secret key directly from the environment
    secret = os.getenv('SECRET_KEY')
    token = jwt.encode({'email': email}, secret, algorithm='HS256')
    return token
