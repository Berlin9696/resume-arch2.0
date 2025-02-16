import boto3
import os
import logging
from flask import current_app
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_s3_client():
    """
    Initializes and returns an S3 client with credentials from Flask config.
    """
    try:
        return boto3.client(
            "s3",
            aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=current_app.config.get("AWS_SECRET_ACCESS_KEY"),
            region_name=current_app.config.get("AWS_REGION", "us-west-2")
        )
    except Exception as e:
        logging.error(f"Failed to initialize S3 client: {e}")
        return None

def upload_to_s3(file, user_id, region, country):
    """
    Uploads a resume to S3 and ensures binary integrity.
    """
    try:
        s3_client = get_s3_client()
        if not s3_client:
            logging.error("S3 client initialization failed.")
            return None

        bucket_name = current_app.config.get("S3_BUCKET_NAME")
        if not bucket_name:
            logging.error("S3 bucket name is missing in configuration.")
            return None

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"

        # Define S3 object key (file path inside bucket)
        file_key = f"{region}/{country}/{filename}"

        # Detect MIME type
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if file.filename.endswith(".docx") else "application/octet-stream"

        # Read file as binary before uploading
        file.seek(0)  # Reset file pointer to beginning
        s3_client.upload_fileobj(
            file,
            bucket_name,
            file_key,
            ExtraArgs={'ContentType': content_type}  # Ensure correct content type
        )

        logging.info(f"File uploaded successfully: {file_key} with ContentType: {content_type}")

        return file_key  # Store only the key in the database

    except Exception as e:
        logging.error(f"S3 Upload Error: {e}")
        return None

def generate_presigned_url(file_key, expiration=300):
    """
    Generates a temporary pre-signed URL for accessing a private S3 file.
    """
    try:
        s3_client = get_s3_client()
        if not s3_client:
            logging.error("S3 client initialization failed.")
            return None

        bucket_name = current_app.config.get("S3_BUCKET_NAME")
        if not bucket_name:
            logging.error("S3 bucket name is missing in configuration.")
            return None

        logging.info(f"Generating pre-signed URL for {file_key} in bucket {bucket_name}")

        # Generate pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_key},
            ExpiresIn=expiration
        )

        logging.info(f"Generated pre-signed URL: {presigned_url}")

        return presigned_url

    except Exception as e:
        logging.error(f"Error generating pre-signed URL: {e}")
        return None

def delete_from_s3(file_key):
    """
    Deletes a file from the S3 bucket.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        s3_client = get_s3_client()
        if not s3_client:
            logging.error("S3 client initialization failed.")
            return False

        bucket_name = current_app.config.get("S3_BUCKET_NAME")
        if not bucket_name:
            logging.error("S3 bucket name is missing in configuration.")
            return False

        # Delete the file
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)

        logging.info(f"Deleted file from S3: {file_key}")

        return True

    except Exception as e:
        logging.error(f"Error deleting file from S3: {e}")
        return False
