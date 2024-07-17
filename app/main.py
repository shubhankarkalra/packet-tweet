from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from celery import Celery
from app.routers import tweet
from app.services.twitter_webhook import TwitterWebhookService
from app.tasks import process_new_tweet
import os

app = FastAPI()

# Celery setup
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

app.include_router(tweet.router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")

twitter_webhook_service = TwitterWebhookService()

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/webhook/twitter")
async def twitter_webhook(request: Request):
    signature = request.headers.get('x-twitter-webhooks-signature')
    raw_data = await request.body()
    
    if twitter_webhook_service.validate_webhook(raw_data, signature):
        data = await request.json()
        if 'tweet_create_events' in data:
            for tweet in data['tweet_create_events']:
                if tweet['user']['id_str'] == os.environ.get("ELON_MUSK_TWITTER_ID"):
                    process_new_tweet.delay(tweet['id_str'])
        return JSONResponse(content={"success": True})
    else:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
