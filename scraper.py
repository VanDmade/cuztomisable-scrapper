from core.fetcher import fetch
from core.parser import parse
from core.checker import check
from config import config
import json
from pathlib import Path

def main():
    url = "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
    checker = check(url)
    if checker == "UNSAFE":
        print("UNSAFE (Disallowed by robots.txt)")
        return False
    # Gets the contents from the domain
    response = fetch(url)
    # Parses the content to get the information the user is looking for
    response = parse(response, value="product_pod")
    for row in response:
        image_containers = parse(row, value="image_container")
        title = parse(row, attribute="title")
        for image_container in image_containers:
            alt = parse(image_container, attribute="alt")
            image = parse(image_container, attribute="src")
        one_star = parse(row, value="One", boolean_response=True)
        two_star = parse(row, value="Two", boolean_response=True)
        three_star = parse(row, value="Three", boolean_response=True)
        four_star = parse(row, value="Four", boolean_response=True)
        five_star = parse(row, value="Five", boolean_response=True)
        print(title)
        print(1 if one_star else (2 if two_star else (3 if three_star else (4 if four_star else 5))))
        print("\n")

if __name__ == "__main__":
    main()
