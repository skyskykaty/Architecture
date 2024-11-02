from flask import Flask, request, jsonify
import random

app = Flask(__name__)

SCORES = {
    'sasha': 5,
    'masha': 7,
    'dasha': 3
}


@app.route('/score', methods=['GET'])
def score():
    username = request.args.get('username')
    if username:
        rating = SCORES[username]
        return jsonify({"username": username, "score": rating})
    return jsonify({"error": "Username is required"}), 400


if __name__ == '__main__':
    app.run(port=5001)  # Запуск на порту 5001
