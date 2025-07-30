from core.parser import parse
from config import config

def respond(html, items):
    response = []
    for item in items:
        params = {
            item.get("type"): item.get("value"),
            "boolean_response": item.get("boolean_response", False)
        }
        content = parse(html, **params)
        key = item.get("key") or item.get("value")
        array = {}
        if isinstance(content, bool):
            array[key] = content if item.get("keep", True) else None
            response.append(array)
            continue
        for counter, row in enumerate(content):
            if counter not in array:
                array[counter] = {}
            nested_items = respond(row, item.get("scrape")) if "scrape" in item else []
            if nested_items:
                array[counter][key] = {
                    config["keys"]["data"]: row if item.get("keep", True) else None,
                    config["keys"]["elements"]: nested_items
                }
            else:
                # Determines if the scraper wants to check for a specific value and if it is true/false
                if "check_for" in item:
                    array[counter][key] = True if item.get("check_for") in row else False
                else:
                    array[counter][key] = row if item.get("keep", True) else None
        if len(array) == 1:
            new_array = {}
            new_array[key] = array[counter][key]
            array = new_array
        response.append(array)
    return merge(response)

def merge(obj):
    if isinstance(obj, list):
        # Check if list is all dicts with one key
        if all(isinstance(i, dict) and len(i) == 1 for i in obj):
            merged = {}
            for i in obj:
                key, value = next(iter(i.items()))
                merged[key] = merge(value)
            return merged
        else:
            return [merge(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: merge(v) for k, v in obj.items()}
    return obj