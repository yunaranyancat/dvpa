import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/login')
def login():
    # Get username and password from the URL query string
    username = request.args.get('username')
    password = request.args.get('password')
    
    # BAD CODE: Constructing a SQL query using string concatenation is vulnerable to SQL injection attacks
    # query = "SELECT * FROM users WHERE name = '" + username + "' AND password = '" + password + "'"
    
    # GOOD CODE: Use a parameterized query to prevent SQL injection attacks
    query = "SELECT * FROM users WHERE name = ? AND password = ?"
    
    # Connect to the database and execute the query using a cursor
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # BAD CODE: Passing user input directly to the execute() method is vulnerable to SQL injection attacks
    # cursor.execute(query)
    
    # GOOD CODE: Pass user input as a parameter to the execute() method to prevent SQL injection attacks
    cursor.execute(query, (username, password,))
    
    # Fetch the results and close the database connection
    rows = cursor.fetchall()
    conn.close()
    
    # Check if a matching record was found
    if len(rows) > 0:
        return "Login successful!"
    else:
        return "Invalid username or password."

if __name__ == '__main__':
    app.run()
