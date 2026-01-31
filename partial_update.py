import requests

endpoint = "http://localhost:8000/api/products/4/"

data = {
    'price':'1.9',
}

response = requests.patch(endpoint, json=data)

print(response.json())
print(response.status_code)