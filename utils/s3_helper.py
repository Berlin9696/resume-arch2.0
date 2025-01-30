# utils/s3_helper.py
import boto3
from flask import current_app
from datetime import datetime

def upload_to_s3(file, user_id):  # <-- MUST EXIST
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{user_id}_{timestamp}_{file.filename}"
    
    s3.upload_fileobj(
        file,
        current_app.config['S3_BUCKET_NAME'],
        filename
    )
    return filename