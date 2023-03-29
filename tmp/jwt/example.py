import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Get the user's credentials from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Verify the user's credentials and retrieve their information
    user = verify_user_credentials(username, password)

    if user:
        # Create a JWT token with the user's information
        payload = {'user_id': user.id, 'username': user.username}
        secret_key = 'my-secret-key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Return the token to the client
        return jsonify({'token': token.decode('utf-8')})

    # Return an error if the user's credentials are invalid
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    # Get the token from the request
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        # Decode the token and retrieve the user's information
        secret_key = 'my-secret-key'
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Retrieve the user's information from the payload
        user_id = payload['user_id']
        username = payload['username']

        # Use the user's information to retrieve their data from the database
        user_data = retrieve_user_data(user_id)

        # Return the user's data to the client
        return jsonify({'user_data': user_data})

    except jwt.exceptions.DecodeError:
        # Return an error if the token is invalid
        return jsonify({'error': 'Invalid token'}), 401
