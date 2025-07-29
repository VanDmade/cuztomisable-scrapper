from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = [h2.get_text() for h2 in soup.find_all("h2")]
    return {"titles": titles}
