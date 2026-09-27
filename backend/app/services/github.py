import os
import requests
from github import Github, Auth

def fetch_pr_diff(repo_full_name: str, pr_number:int, installation_id: int) -> str:
    app_id = int(os.environ.get("GITHUB_APP_ID"))
    private_key_path = os.environ.get("GITHUB_PRIVATE_KEY", "private-key.pem")

    with open(private_key_path, "r") as key_file:
        private_key = key_file.read()

    auth = Auth.AppAuth(app_id, private_key).get_installation_auth(installation_id)
    g = Github(auth=auth)

    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    headers = {
        "Authorization" : f"Bearer {auth.token}",
        "Accept" : "application/vnd.github.v3.diff"
    }

    response = requests.get(pr.url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch PR diff: {response.status_code} - {response.text}")