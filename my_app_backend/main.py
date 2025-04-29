from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from context.context_hsm import ContextHSM 
from hsm_models.role_handler import get_user_role

app = Flask(__name__)
CORS(app)

context = ContextHSM()
authorized = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    headers = request.headers
    auth = headers.get('Authorization')
    if not auth:
        return {'statusCode': 401, 'error': 'Authorization header is missing'}
    if auth[0:6] == "Basic ":
        auth = auth[6:]
    autheticated, message = context.login.authenticate(auth)
    if not autheticated:
        return {'statusCode': 401, 'error': message}
    session_token = context.session_manager.create_session(auth)
    response = {'statusCode': 200, 'message': 'success', 'sessionToken': session_token}
    return response

# @app.route('/api/create_user', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     if not data:
#         return {'statusCode': 400, 'error': 'Invalid input'}
#     username = data.get('username')
#     password = data.get('password')
#     role = data.get('role')
#     if not username or not password or not role:
#         return {'statusCode': 400, 'error': 'Missing required fields'}
#     user_role = get_user_role(role, username, password)
#     status, message = context.login.create(user_role)
#     if not status:
#         return {'statusCode': 500, 'error': message}
#     return {'statusCode': 201, 'message': message}

@app.route('/appointment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appointments():
    if request.method == 'GET':
        return {'statusCode': 200, 'message': 'GET request successful'}
    elif request.method == 'POST':
        return {'statusCode': 201, 'message': 'POST request successful'}
    elif request.method == 'PUT':
        return {'statusCode': 200, 'message': 'PUT request successful'}
    elif request.method == 'DELETE':
        return {'statusCode': 200, 'message': 'DELETE request successful'}

if __name__ == '__main__':
    app.run(debug=True)
    serve(app, port=5000)