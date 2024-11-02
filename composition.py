from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import grpc

load_dotenv()

app = Flask(__name__)

# Пороговое значение для оценки
SCORE_THRESHOLD = float(os.getenv('SCORE_THRESHOLD', 5.0))


@app.route('/composition', methods=['POST'])
def composition():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Сначала получаем оценку пользователя
    score_response = requests.get(f'http://127.0.0.1:5001/score?username={username}')

    if score_response.status_code != 200:
        user_score = SCORE_THRESHOLD  # Устанавливаем на максимальное значение для успешной авторизации
    else:
        score_data = score_response.json()
        user_score = score_data.get('score', 0)

    if user_score >= SCORE_THRESHOLD:
        auth_response = requests.post('http://127.0.0.1:5002/auth', json={"username": username, "password": password})
        return auth_response.json()

    return jsonify({"auth": False, "message": "Аутентефикация запрещена."})


if __name__ == '__main__':
    app.run(port=5000)  # Запуск на порту 5003
