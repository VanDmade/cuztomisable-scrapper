from core.fetcher import fetch
from core.checker import check
from core.responder import respond
from config import config
from datetime import datetime
import json
import os
import sys
import time

def main():
    start_time = time.time()
    message = checker = data = file = url = None
    if len(sys.argv) > 1:
        file = sys.argv[1] or None
        if os.path.exists(file):
            # Load the file into an array for use
            with open(file, "r", encoding="utf-8") as f:
                scraper = f.read()
            scraper = json.loads(scraper)
            url = scraper["url"] or None
        else:
            # The file doesn't exist or couldn't be found
            message = "The file doesn't currently exist."
        if url is not None:
            checker = "SAFE" #check(url)
            if checker != "UNSAFE":
                # Gets the contents from the domain
                data = fetch(url)
                # Load the file into an array for use
                '''with open("./config/test.txt", "r", encoding="utf-8") as f:
                    data = f.read()'''
                data = respond(data, scraper["scraper"] or None)
            else:
                # The robots.txt file from the site doesn't allow crawling this site
                message = "Scraping this site is not allowed by robots.txt."
        else:
            # The scraper JSON file doesn't follow the correct format
            message = "The scraper JSON file does not contain a URL."
    else:
        # File argument is missing from the script call
        message = "No file argument provided. Usage: python scraper.py <file_path>"
    # Generates the full response for the scraper
    response = {
        "version": config.get("version"),
        "status": checker,
        "file": file,
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "execution_time": round(time.time() - start_time, 5),
        "message": message,
        "data": data
    }
    # Outputs the response
    print(json.dumps(response))
    return

if __name__ == "__main__":
    main()
