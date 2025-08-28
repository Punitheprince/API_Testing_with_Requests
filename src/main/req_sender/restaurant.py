import requests
import json
from bs4 import BeautifulSoup

response_value= ""
restaurant_file_path = '../../resources/req_spec/query_params/restaurant_params.json'

with open(restaurant_file_path, 'r') as file:
    restaurant_data = json.load(file)

query_params= restaurant_data["query_prams"]

header_file_path = '../../resources/req_spec/headers/header.json'
with open(header_file_path, 'r') as file:
    header_data = json.load(file)

with open("headers.json", "w") as f:
    json.dump(header_data, f, indent=4)

base_url="https://www.swiggy.com/dapi/"
resource="restaurants/list/v5"


# print(type(headers))
url= f"{base_url}/{resource}?{query_params}"


#response
response = requests.get(url,headers=header_data)
response_value =response

content_type = response.headers.get("Content-Type", "").lower()

print("headers : ",response.headers)

if "html" in content_type:
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        print("Body :",soup.prettify())
    except Exception:
        print(response.text)
elif "json" in content_type:
    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)
