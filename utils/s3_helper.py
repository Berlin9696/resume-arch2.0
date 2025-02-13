import boto3
import os
from flask import current_app
from datetime import datetime

def upload_to_s3(file, user_id, region, country):
    """
    Uploads a resume to S3 in the appropriate region/country folder.

    Args:
        file (FileStorage): The uploaded file object.
        user_id (int): ID of the user uploading the file.
        region (str): Selected region (AMER, APAC, EMEA).
        country (str): Selected country within the region.

    Returns:
        str: Public URL of the uploaded file if successful, None otherwise.
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        )

        # Define S3 bucket name
        bucket_name = current_app.config['S3_BUCKET_NAME']

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"

        # Define full S3 file path (e.g., "AMER/Canada/12345_resume.pdf")
        file_key = f"{region}/{country}/{filename}"

        # Upload file to S3
        s3_client.upload_fileobj(file, bucket_name, file_key)

        return f"https://{bucket_name}.s3.amazonaws.com/{file_key}"

    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None
