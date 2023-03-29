import jwt

# Set up the payload with the user's information
payload = {'user_id': 1234, 'username': 'johndoe'}

# Encode the payload without a secret key to create the JWT token
token = jwt.encode(payload, algorithm='none')

# Print out the token
print(token)
