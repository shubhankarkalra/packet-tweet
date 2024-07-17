import logging
from fastapi import APIRouter, HTTPException
from app.services.twitter_service import TwitterService
from app.services.screenshot_service import ScreenshotService
from app.services.instagram_service import InstagramService
from app.tasks import process_new_tweet

router = APIRouter()
twitter_service = TwitterService()
instagram_service = InstagramService()

logger = logging.getLogger(__name__)

@router.post("/tweet/{tweet_id}/process")
async def process_tweet(tweet_id: str):
    try:
        logger.info(f"Processing tweet {tweet_id}")
        # Use the existing Celery task to process the tweet
        result = process_new_tweet.delay(tweet_id)
        
        # Wait for the task to complete
        task_result = result.get(timeout=60)  # Adjust timeout as needed
        
        logger.info(f"Task result: {task_result}")
        
        if task_result and 'public_image_url' in task_result:
            return {"success": True, "screenshotUrl": task_result['public_image_url']}
        else:
            logger.error(f"Failed to process tweet. Task result: {task_result}")
            raise HTTPException(status_code=500, detail="Failed to process tweet")
    except Exception as e:
        logger.exception(f"Error processing tweet {tweet_id}")
        raise HTTPException(status_code=500, detail=str(e))