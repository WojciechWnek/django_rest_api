import requests

endpoint = " http://localhost:8000/api/products/1/update/"

data = {
    "title": "Changed title",
    "price": 199.97
}

get_response = requests.put(endpoint, json=data)
print(get_response.json())
