import requests

user = str(input("Введите имя пользователя: "))
passwd = str(input("Введите пароль: "))

# Тут будем отправлять запросы на сервер через порт, который прослушивает NGINX
response = requests.post(f'http://localhost:8080/composition/', json={"username": user, "password": passwd})
print(response.json())