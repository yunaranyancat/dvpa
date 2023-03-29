import jwt

# Set up the payload with the user's information
payload = {'user_id': 5678, 'username': 'janedoe'}

# Replace the second segment of the token with the modified payload
token_parts = token.split('.')
token_parts[1] = jwt.encode(payload, algorithm='none').decode('utf-8')
modified_token = '.'.join(token_parts)

# Print out the modified token
print(modified_token)
