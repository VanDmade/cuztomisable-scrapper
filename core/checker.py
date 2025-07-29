import requests
from config import config

def check(url):
    # Sets up the URL to be used to check the robots.txt file
    url, url_path, url_query = setup_url(url)
    response = requests.get(url, headers=config.get("headers"), timeout=config.get("timeout", 5))
    # Checks to make sure the robots.txt file exist
    if response.status_code == 404 or url_path == "":
        return "SAFE_WITH_WARNING"
    response.raise_for_status()
    # Iterates through the files and gets all of the disallowed paths
    for line in response.text.splitlines():
        if " " not in line:
            # The line doesn't contain the correct information
            continue
        # TODO :: Check for the base path i.e. /admin/* should not allow anything after /admin
        allowed, path = line.split(" ", 1)
        path = path.strip("/")
        if path == url_path:
            return "SAFE" if allowed.strip(":").lower() == "allow" else "UNSAFE"
    return "SAFE"

def setup_url(url):
    url = url.lower()
    https = True if url.startswith("https://") else False
    # Cleans the URL so everything is appropriately setup for the functionality
    url = url.lstrip("https://").lstrip("http://").rstrip("/")
    path = query = ""
    # If there is a path string
    if "/" in url:
        url, path = url.split("/", 1)
    # If there is a query string
    if "?" in path:
        path, query = path.split("?", 1)
    path = path.strip("/")
    url = ("https://" if https else "http://") + url + "/robots.txt"
    return url, path, query
