import os
import jwt
from itsdangerous import URLSafeTimedSerializer

# Ensure SECRET_KEY and SECURITY_PASSWORD_SALT are set
SECRET_KEY = os.getenv("SECRET_KEY")
SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

if not SECRET_KEY or not SECURITY_PASSWORD_SALT:
    raise ValueError("Missing SECRET_KEY or SECURITY_PASSWORD_SALT in environment variables")

# Token generation using itsdangerous (Timed Token - for email/password reset)
def generate_timed_token(email):
    """Generate a secure, time-sensitive token for email confirmation and password reset."""
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_timed_token(token, expiration=3600):
    """Confirm the time-sensitive token and extract the email if valid."""
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=expiration)
        return email
    except Exception as e:
        print(f"Error in confirm_timed_token: {e}")
        return False

# Token generation using JWT (General Authentication - for API or user session)
def generate_jwt_token(email):
    """Generate a JWT token for authentication."""
    token = jwt.encode({'email': email}, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token):
    """Verify a JWT token and extract the email if valid."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded.get("email")
    except jwt.ExpiredSignatureError:
        print("JWT Token has expired")
        return False
    except jwt.InvalidTokenError:
        print("Invalid JWT Token")
        return False
