import requests

endpoint = "http://localhost:8000/api/products/2/"

data = {
    'name':'kiwi',
    'price':'1500',
    'email':'Kiwi@gmail.com',# champ obligatoire 
    'description':'Fruit tres sucre de couleur rouge'
}

response = requests.put(endpoint, json=data)

print(response.json())
print(response.status_code)