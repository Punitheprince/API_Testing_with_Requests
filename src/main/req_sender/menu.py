import requests
import json
import re

from src.main.utils import helper
from bs4 import BeautifulSoup

# -------------------------------
# File paths
# -------------------------------
query_param_file_path = '../../resources/req_spec/query_params/menu_params.json'
default_json_file_path = '../../resources/config/default_config.json'
# -------------------------------
# API base URL + resource
# -------------------------------
base_url = "https://www.swiggy.com/dapi"
resource = "restaurants/list/v5"
url = f"{base_url}/{resource}"

# -------------------------------
# Function: Resolve placeholders
# -------------------------------
def resolve_placeholders(query_file, data_file):
    """
    Reads query_file JSON, replaces <placeholders>
    with values from data_file JSON (works for nested dicts/lists).
    """
    with open(query_file, 'r') as f:
        query_json = json.load(f)
    with open(data_file, 'r') as f:
        data_map = json.load(f)

    pattern = re.compile(r"<(.*?)>")

    def replace_placeholders(value):
        if isinstance(value, str):
            match = pattern.search(value)
            if match:
                key = match.group(1)
                return data_map.get(key, value)  # replace only if found
            return value
        elif isinstance(value, dict):
            return {k: replace_placeholders(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_placeholders(v) for v in value]
        return value

    return replace_placeholders(query_json)

# -------------------------------
# Resolve placeholders from config
# -------------------------------
resolved_params = resolve_placeholders(query_param_file_path, default_json_file_path)
print("Resolved Params:\n", json.dumps(resolved_params, indent=4))

# -------------------------------
# Send GET request
# -------------------------------
response = requests.get(url, headers=helper.get_headers(), params=resolved_params)

print("Final URL:", response.url)
print("Status:", response.status_code)

# -------------------------------
# Beautify response
# -------------------------------
content_type = response.headers.get("Content-Type", "").lower()

if "json" in content_type:
    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)
elif "html" in content_type:
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        print("Body:", soup.prettify())
    except Exception:
        print(response.text)
else:
    print(response.text)
