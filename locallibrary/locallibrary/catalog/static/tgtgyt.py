import requests

URL = 'https://reqres.in/api/users'
t = requests.get(URL).json()
print(t, '')