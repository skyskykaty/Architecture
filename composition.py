from flask import Flask, request, jsonify
import grpc
import score_pb2
import score_pb2_grpc
import auth_pb2
import auth_pb2_grpc
import os
from dotenv import load_dotenv

# AuthRequest = auth_pb2._globals.get('AuthRequest')
# AuthResponse = auth_pb2._globals.get('AuthResponse')

load_dotenv()

app = Flask(__name__)

# Пороговое значение для оценки
SCORE_THRESHOLD = float(os.getenv('SCORE_THRESHOLD', 5.0))


def get_score(username):
    with grpc.insecure_channel('localhost:5001') as channel:
        stub = score_pb2_grpc.ScoreServiceStub(channel)
        tmp = score_pb2.ScoreRequest(username=username)
        response = stub.GetScore(tmp)

        return response.score


def auth(username, password):
    with grpc.insecure_channel('localhost:5002') as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        tmp = auth_pb2.AuthRequest(username=username, password=password)
        response = stub.Auth(tmp)

        # response = stub.Auth(AuthRequest(username=username, password=password))
        return response.auth


@app.route('/composition', methods=['POST'])
def composition():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Сначала получаем оценку пользователя
    try:
        user_score = get_score(username)
        if user_score >= SCORE_THRESHOLD:
            is_authenticated = auth(username, password)
            if is_authenticated:
                return jsonify({"auth": True})

        return jsonify({"auth": False, "message": "Аутентификация запрещена."})

    except Exception as e:
        print(e)
        return jsonify({"auth": True})


if __name__ == '__main__':
    app.run(port=5000)  # Запуск на порту 5000

'python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. score.proto'