# updater_service.py

import requests
import subprocess
import os

def get_latest_release_info(repo_owner, repo_name):
    try:
        # Fetch information about the latest release
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        response = requests.get(url)
        response.raise_for_status()

        release_info = response.json()
        download_url = release_info["assets"][0]["browser_download_url"]

        return download_url
    except Exception as e:
        print(f"Error: {e}")
        return None

def download_and_apply_update(url, target_folder, target_name):
    try:
        # Download the updated file
        os.system(f"wget {url} -O {target_folder}/{target_name}")

        # Run the updated file
        subprocess.Popen(["python3", f"{target_folder}/{target_name}"])

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    owner = "GamePlay"
    market_repo = "MCMarket"

    # Update the Market app (assumed to be the main app)
    market_latest_release_url = get_latest_release_info(owner, market_repo)

    if market_latest_release_url:
        target_folder = "."  # Assuming the main app script is in the current directory
        target_name = "market_app.py"

        if download_and_apply_update(market_latest_release_url, target_folder, target_name):
            print("Market app (MediaCall Market) update applied successfully.")
        else:
            print("Market app (MediaCall Market) update failed.")
