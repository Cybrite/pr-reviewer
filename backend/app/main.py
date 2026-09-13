from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

from app.core.security import verify_github_signature

app = FastAPI(title = "Algorithmic PR reviewer")

@app.post("/webhook")
async def github_webhook(request: Request, event: str = Header(None, alias="X-GitHub-Event")):
    await verify_github_signature(request)

    payload = await request.json()

    if event != "pull_request":
        return {"status": "ignored", "message": f"Event '{event}' is not handled."}

    action = payload.get("action")

    if action not in ["opened", "synchronize"]:
        return {"status": "ignored", "message": f"Action '{action}' is not handled."}

    pr_number = payload["pull_request"]["number"]
    repo_full_name = payload["repository"]["full_name"]

    print(f"Received valid PR webhook {repo_full_name}#{pr_number} with action '{action}'.")

    return {"status": "success", "message": "webhook processed successfully."}