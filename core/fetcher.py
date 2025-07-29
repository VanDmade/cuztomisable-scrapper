import requests
from config import config

def fetch(url):
    response = requests.get(url, headers=config.get("headers"), timeout=config.get("timeout", 5))
    # The URL is invalid and not able to be used
    if response.status_code == 404:
        return False
    response.raise_for_status()
    # Minifies the text to reduce space if stored
    return minify(response.text)

def minify(content):
    minified = ""
    for line in content.splitlines():
        # Makes sure the line isn't empty
        if line.strip():
            minified = minified + line.strip(" ")
    return minified