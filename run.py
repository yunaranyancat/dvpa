from flask import Flask,request,jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

UPLOADS = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOADS

users = {
    "admin": generate_password_hash("admin"),
    "susan": generate_password_hash("susan")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

@app.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if username in users:
        abort(400)
    users[username] = generate_password_hash(password)
    return jsonify({'created' : True}), 201

@app.route('/greet/<user>')
def greet(user):
    output = subprocess.getoutput("echo Hello " + user)
    return jsonify({'result' : output}), 200

@app.route('/upload', methods = ['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error' : 'Unsupported format'}), 400

    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        success = True

    if success:
        return jsonify({'success' : 'File has been successfully uploaded'}), 200
    else:
        return jsonify({'error' : 'Server encountered some error'}), 500

if __name__ == '__main__':
    app.run()
