import requests

endpoint = "http://localhost:8000/api/"

data = {
    'name' : 'avocat',
    'price' : 1000,
    'description' : 'fruit a noyau'
}

response = requests.get(endpoint)

print(response.json())
print(response.status_code)