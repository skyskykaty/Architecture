from flask import Flask, request, jsonify

app = Flask(__name__)

PASSWDS = {
    'sasha': 'qwerty123',
    'masha': '12345',
    'dasha': 'qwerty',
    'katya': 'humble'
}


@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if PASSWDS[username] == password:
        return jsonify({"auth": True})
    return jsonify({"auth": False})


if __name__ == '__main__':
    app.run(port=5002)  # Запуск на порту 5002
