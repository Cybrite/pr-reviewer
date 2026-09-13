import hmac
import hashlib
import os
from fastapi import HTTPException, Request

async def verify_github_signature(request: Request):
    signature_header = request.headers.get("X-Hub-Signature-256")
    if not signature_header:
        raise HTTPException(status_code=401, detail="Missing X-Hub-Signature-256 header")

    secret = os.environ.get("GITHUB_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="GitHub webhook secret not configured")

    payload = await request.body()

    hash_object = hmac.new(
        secret.encode("utf-8"),
        msg = payload,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=401, detail="Invalid signature")
