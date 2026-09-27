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

    installation_id = payload["installation"]["id"]

    print(f"\nIntercepted PR: {repo_full_name}#{pr_number}")
    print("Fetching raw code diff...")

    try:
        diff_text = fetch_pr_diff(repo_full_name, pr_number, installation_id)
        print("Sucess! diff length:", len(diff_text))
        print("Diff preview (first 500 chars):\n", diff_text[:500])
    except Exception as e:
        print("Error fetching PR diff:", str(e))
        return {"status": "error", "message": str(e)}

    return {"status": "success", "message": "webhook processed successfully."}