import hmac
import hashlib
import os

class TwitterWebhookService:
    def __init__(self):
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")

    def validate_webhook(self, payload, header_signature):
        local_signature = hmac.new(
            key=self.consumer_secret.encode('utf-8'),
            msg=payload,
            digestmod=hashlib.sha256
        )
        local_signature_b64 = base64.b64encode(local_signature.digest()).decode('ascii')
        return hmac.compare_digest(local_signature_b64, header_signature.split('=', 1)[1])
