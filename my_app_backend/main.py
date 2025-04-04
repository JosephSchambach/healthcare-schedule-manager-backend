from flask import Flask, request
from waitress import serve
from context.context_hsm import ContextHSM 

app = Flask(__name__)

context = ContextHSM()
authorized = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/login', methods=['POST'])
def login():
    headers = request.headers
    auth = headers.get('Authorization')
    if not auth:
        return {'error': 'Authorization header is missing'}, 401
    autheticated, message = context.authenticator.authenticate(auth)
    if not autheticated:
        return {'error': message}, 401
    session_token = context.session_manager.create_session(auth)
    response = {'message': 'Authenticated successfully', 'session_token': session_token}
    return response, 200

@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.json



if __name__ == '__main__':
    app.run(debug=True)
    serve(app, port=5000)