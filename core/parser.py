import re

def parse(content, tag=None, attribute=None, value=None, boolean_response=False):
    response = []
    # Determine what to search for
    if tag is not None:
        search_value = f"<{tag}"
    elif attribute is not None:
        search_value = f'{attribute}='
    elif value is not None:
        search_value = value
    else:
        # Nothing to search for
        return response
    # Loop until no match is found
    while search_value in content:
        if attribute:
            data, content = find_attribute(content, attribute)
        elif tag:
            data, content = find_tag(content, tag)
        else:
            data, content = find(content, search_value)
        if not data:
            # Stop if no data was extracted
            break
        response.append(data)
    if boolean_response:
        return bool(response and response[0])
    return response

def find(content, value):
    pattern = fr"{value}"
    # Finds the location where the first instance exists
    match = re.search(pattern, content)
    before, after = split_into_two(content.split(f"{value}", 1))
    # Gets the tag of the class
    tag = before.split("<")[-1].split(" ")[0]
    before, after = split_into_two(after.split(">", 1))
    data, after = split_into_two(after.split(f"</{tag}", 1))
    return data, after

def find_tag(content, value):
    pattern = fr"<{value}(?:\s|>)"
    # Finds the location where the first instance exists
    match = re.search(pattern, content)
    before, after = split_into_two(re.split(pattern, content, maxsplit=1))
    data, after = split_into_two(after.split(f"</{value}>", 1))
    # If for some reason the tag has other attributes
    if match and match.group().endswith(" "):
        data = data.split(">", 1)[1]
    data = data.strip(" ")
    return data, after

def find_attribute(content, value):
    before, after = split_into_two(content.split(f" {value}=", 1))
    # Allows for single or double quotes to be used
    single = False if after[0] == "\"" else True
    after = after.lstrip("\"").lstrip("'")
    data, after = split_into_two(after.split("\"" if not single else "'", 1))
    return data, after

def split_into_two(value):
    return (value + [""])[:2]