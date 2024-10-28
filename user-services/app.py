from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "User 1",
        "email": "3E1aA@example.com",
        "age": 25
    },
    {
        "id": 2,
        "name": "User 2",
        "email": "Gv7Gg@example.com",
        "age": 30
    }
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, port=3001)  