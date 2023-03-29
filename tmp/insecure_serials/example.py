from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

# Sample class to be serialized
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Sample API endpoint that returns a serialized User object
@app.route('/user', methods=['GET'])
def get_user():
    user = User('John Doe', 'johndoe@example.com')
    serialized_user = pickle.dumps(user)
    return jsonify({'user': serialized_user})

# Sample API endpoint that accepts a serialized User object and returns it
@app.route('/user', methods=['POST'])
def create_user():
    serialized_user = request.get_json()['user']
    user = pickle.loads(serialized_user)
    return jsonify({'user': user.__dict__})

if __name__ == '__main__':
    app.run(debug=True)
