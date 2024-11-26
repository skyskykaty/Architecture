from flask import Flask, jsonify, request
from flask_smorest import Api, Blueprint
import grpc
import score_pb2
import score_pb2_grpc
import auth_pb2
import auth_pb2_grpc
import os
from dotenv import load_dotenv

load_dotenv()

SCORE_THRESHOLD = float(os.getenv('SCORE_THRESHOLD', 5.0))

app = Flask(__name__)

app.config["API_TITLE"] = "User Authentication and Score API"
app.config["API_VERSION"] = "1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.0"
app.config["OPENAPI_SPEC"] = "openapi.yaml"

api = Api(app)

blp = Blueprint("Composition", "composition", url_prefix="/composition",
                description="Аутентификация пользователя и оценка")

def get_score(username):
    with grpc.insecure_channel('score:5001') as channel:
        stub = score_pb2_grpc.ScoreServiceStub(channel)
        tmp = score_pb2.ScoreRequest(username=username)
        response = stub.GetScore(tmp)
        return response.score


def auth(username, password):
    with grpc.insecure_channel('auth:5002') as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        tmp = auth_pb2.AuthRequest(username=username, password=password)
        response = stub.Auth(tmp)
        return response.auth


@blp.route("/", methods=["POST"])
@blp.response(200, {
    "auth": bool,
    "message": str
})
@blp.response(400, {
    "auth": bool,
    "message": str
})
@blp.response(500, {
    "auth": bool,
    "message": str
})
def composition():
    """
    Проверяет оценку пользователя и выполняет аутентификацию.
    Если оценка выше порога, запрашивает аутентификацию.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        user_score = get_score(username)
        if user_score >= SCORE_THRESHOLD:
            is_authenticated = auth(username, password)
            if is_authenticated:
                return jsonify({"auth": True, "message": "Аутентификация успешна."})

        return jsonify({"auth": False, "message": "Аутентификация запрещена."})

    except Exception as e:
        print(e)
        return jsonify({"auth": False, "message": "Ошибка при обработке запроса."}), 500



api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
