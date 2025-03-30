"""
Debug script to test S3 connection and configuration.
Run with: python debug_s3.py
"""
import os
import sys
import django
import traceback

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fspapplication_backend.settings')
django.setup()

from fspapplication_backend.files.s3_utils import S3Client
from django.conf import settings

print("\n=== S3 Connection Test ===\n")

# Print S3 configuration (with redacted credentials)
print(f"AWS Region: {settings.AWS_S3_REGION_NAME}")
print(f"AWS Bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"AWS Access Key ID: {settings.AWS_ACCESS_KEY_ID[:4]}{'*' * 16}")
print(f"AWS Secret Access Key: {'*' * 20}")

# Test S3 connection
try:
    print("\nInitializing S3 client...")
    s3_client = S3Client()
    
    print("\nTesting connection to S3...")
    import boto3
    client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    # List buckets
    print("\nListing buckets...")
    response = client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print(f"Available buckets: {buckets}")
    
    # Check if bucket exists
    bucket_exists = settings.AWS_STORAGE_BUCKET_NAME in buckets
    print(f"Bucket {settings.AWS_STORAGE_BUCKET_NAME} exists: {bucket_exists}")
    
    if not bucket_exists:
        print("\nERROR: Configured bucket does not exist! Please create the bucket or update settings.")
    
    # Test a small upload
    if bucket_exists:
        print("\nTesting file upload...")
        # Create a small test file
        test_filename = "s3_test_file.txt"
        with open(test_filename, "w") as f:
            f.write("This is a test file for S3 upload.")
        
        # Open the file for upload
        with open(test_filename, "rb") as f:
            test_key = "test/s3_test_file.txt"
            try:
                client.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, test_key)
                print(f"Test file uploaded successfully to {test_key}")
                
                # Generate a presigned URL
                url = client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                        'Key': test_key
                    },
                    ExpiresIn=3600
                )
                print(f"Presigned URL generated: {url[:60]}...")
                
                # Clean up the test file
                client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=test_key
                )
                print(f"Test file deleted from S3")
            except Exception as e:
                print(f"ERROR during test upload: {str(e)}")
                traceback.print_exc()
        
        # Clean up local test file
        if os.path.exists(test_filename):
            os.remove(test_filename)
            
except Exception as e:
    print(f"\nERROR: {str(e)}")
    traceback.print_exc()

print("\n=== End of S3 Connection Test ===\n") 