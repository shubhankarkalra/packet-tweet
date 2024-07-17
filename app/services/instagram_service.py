import requests
import os
from fastapi import HTTPException

class InstagramService:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.api_base_url = "https://graph.facebook.com/v12.0"

    def post_image(self, image_url, caption):
        # First, create a container for the post
        container_id = self._create_media_container(image_url, caption)
        
        # Then, publish the container
        return self._publish_media(container_id)

    def _create_media_container(self, image_url, caption):
        url = f"{self.api_base_url}/{self.instagram_account_id}/media"
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        response = requests.post(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to create media container")
        return response.json()["id"]

    def _publish_media(self, container_id):
        url = f"{self.api_base_url}/{self.instagram_account_id}/media_publish"
        params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        response = requests.post(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to publish media")
        return response.json()["id"]