from celery import shared_task
import boto3
import os
from botocore.exceptions import ClientError

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def upload_to_public_url(file_path):
    bucket_name = os.getenv('S3_BUCKET_NAME')
    object_name = os.path.basename(file_path)
    
    try:
        s3_client.upload_file(file_path, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return None

    # Construct the public URL
    return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

# Update the process_new_tweet function to use this new upload function
@shared_task
def process_new_tweet(tweet_id):
    screenshot_service = ScreenshotService()
    instagram_service = InstagramService()

    tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
    
    # Capture screenshot
    screenshot = screenshot_service.capture_screenshot(tweet_url)
    
    # Save screenshot to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(screenshot)
        temp_file_path = temp_file.name

    try:
        # Upload the image to S3 and get the public URL
        public_image_url = upload_to_public_url(temp_file_path)
        
        if public_image_url:
            # Post to Instagram
            instagram_service.post_image(public_image_url, caption=f"New tweet from Elon Musk: {tweet_url}")
        else:
            print("Failed to upload image to S3")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)