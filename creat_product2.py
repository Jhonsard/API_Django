import requests

endpoint = "http://localhost:8000/api/products/"

data = {
    'name' : 'ananas',
    'price' : 1000,
    'description' : 'fruit a noyau'
}

response = requests.get(endpoint, json=data)

print(response.json())
print(response.status_code)