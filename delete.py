import requests

endpoint = "http://localhost:8000/api/products/4/"

response = requests.delete(endpoint)

print(response.json())
print(response.status_code)