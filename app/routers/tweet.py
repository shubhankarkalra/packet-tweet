from fastapi import APIRouter, HTTPException, Response
from app.services.twitter_service import TwitterService
from app.services.screenshot_service import ScreenshotService

router = APIRouter()
twitter_service = TwitterService()

@router.get("/tweet/{tweet_id}/screenshot")
async def get_tweet_screenshot(tweet_id: str):
    try:
        tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
        screenshot = await ScreenshotService.capture_screenshot(tweet_url)
        return Response(content=screenshot, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))