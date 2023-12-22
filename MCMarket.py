import os
import subprocess
import threading
import requests
import webview
from tkinter import Tk, Button, messagebox

from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

owner = "your_username"
installer_repo = "installer_repo"

apps = [
    {"name": "app1", "repo_owner": "app1_owner", "repo_name": "app1_repo", "install_command": "sudo apt-get install -y app1", "icon_path": "/path/to/app1/icon.png"},
    {"name": "app2", "repo_owner": "app2_owner", "repo_name": "app2_repo", "install_command": "sudo apt-get install -y app2", "icon_path": "/path/to/app2/icon.png"},
    # Add more apps as needed
]

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

def download_and_install(url, target_folder, install_command):
    try:
        # Download the file
        os.system(f"wget {url} -O {target_folder}.tar.gz")

        # Extract the file
        os.system(f"tar -zxvf {target_folder}.tar.gz")

        # Run the installation command
        os.system(f"{install_command}")

        # Remove the compressed file
        os.system(f"rm {target_folder}.tar.gz")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def add_shortcut_to_menu(app_name, executable_path, icon_path):
    os.system(f'lxpanelctl add {app_name} -p {executable_path} -i {icon_path}')

def add_shortcut_to_desktop(app_name, executable_path, icon_path):
    desktop_file_path = os.path.expanduser(f"~/Desktop/{app_name}.desktop")
    os.system(f"lxshortcut -o {desktop_file_path} -i {icon_path} -e {executable_path}")

class AppUpdater:
    def __init__(self, master):
        self.master = master
        self.master.title("MediaCall Market Installer")

        # Add an "Update Market" button
        self.update_button = Button(self.master, text="Update Market", command=self.update_market)
        self.update_button.pack()

    def update_market(self):
        market_owner = "GamePlay-Tech"
        market_repo = "MCMarket"
        
        latest_release_url = get_latest_release_info(market_owner, market_repo)

        if latest_release_url:
            target_folder = "."  # Assuming the main app script is in the current directory
            target_name = "MCMarket.py"

            if download_and_install(latest_release_url, target_folder, target_name):
                messagebox.showinfo("Update Successful", "MediaCall Market has been updated successfully.")
            else:
                messagebox.showerror("Update Failed", "Failed to update MediaCall Market.")
        else:
            messagebox.showinfo("Already Up to Date", "MediaCall Market is already up to date.")

def run_flask_app():
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))

def open_browser():
    webview.create_window("My Flask App", "http://localhost:5000/")

def install_apps():
    for app in apps:
        repo_owner = app["repo_owner"]
        repo_name = app["repo_name"]
        download_url = get_latest_release_info(repo_owner, repo_name)

        if download_url:
            app_name = app["name"]
            icon_path = app["icon_path"]

            target_folder = f"/path/to/{app_name}"
            install_command = app["install_command"]

            if download_and_install(download_url, target_folder, install_command):
                add_shortcut_to_menu(app_name, f"{target_folder}/executable", icon_path)
                add_shortcut_to_desktop(app_name, f"{target_folder}/executable", icon_path)

if __name__ == '__main__':
    installer_thread = threading.Thread(target=install_apps)
    installer_thread.start()

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    root = Tk()
    updater = AppUpdater(root)
    root.mainloop()

    import time
    time.sleep(2)

    open_browser()
