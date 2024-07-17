from celery import shared_task
import tempfile
import os
import logging
from app.services.screenshot_service import ScreenshotService
from app.services.instagram_service import InstagramService
from app.utils import upload_to_public_url

logger = logging.getLogger(__name__)

@shared_task
def process_new_tweet(tweet_id):
    logger.info(f"Starting to process tweet {tweet_id}")
    screenshot_service = ScreenshotService()
    instagram_service = InstagramService()

    tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
    
    try:
        # Capture screenshot
        logger.info("Capturing screenshot")
        screenshot = screenshot_service.capture_screenshot(tweet_url)
        
        # Save screenshot to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(screenshot)
            temp_file_path = temp_file.name

        try:
            # Upload the image to S3 and get the public URL
            logger.info("Uploading to S3")
            public_image_url = upload_to_public_url(temp_file_path)
            
            if public_image_url:
                # Post to Instagram
                logger.info("Posting to Instagram")
                instagram_service.post_image(public_image_url, caption=f"New tweet from Elon Musk: {tweet_url}")
                logger.info("Process completed successfully")
                return {"public_image_url": public_image_url}
            else:
                logger.error("Failed to upload image to S3")
                return None
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    except Exception as e:
        logger.exception(f"Error processing tweet {tweet_id}")
        return {"error": str(e)}