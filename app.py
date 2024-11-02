import requests

user = str(input("Введите имя пользователя: "))
passwd = str(input("Введите пароль: "))

response = requests.post(f'http://127.0.0.1:5000/composition', json={"username": user, "password": passwd})
print(response.json())
