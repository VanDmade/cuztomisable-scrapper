from core.fetcher import fetch_html
from core.parser import parse_html
from core.saver import save_to_json
import json
from pathlib import Path

# Load settings
config = json.loads(Path("config/settings.json").read_text())

def main():
    url = config["url"]
    html = fetch_html(url)
    data = parse_html(html)
    save_to_json(data, config["output_file"])
    print(f"✅ Data saved to {config['output_file']}")

if __name__ == "__main__":
    main()
