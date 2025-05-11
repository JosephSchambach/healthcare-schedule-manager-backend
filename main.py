from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from my_app_backend.context.context_hsm import ContextHSM 
from my_app_backend.hsm_models.patient import CreatePatientAppointment, PatientAppointment, UpdatePatientAppointment, DeletePatientAppointment, GetPatientAppointments

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
def appointment():
    if request.method == 'GET':
        """
            Requires columns and a condition in the request body to filter the appointment details.
            Returns appointment details in a json structure of rows and columns
        """
        try:
            data = request.get_json()
            if not data: 
                return {'statusCode': 400, 'error': 'Invalid input'}
            condition = data.get('condition')
            if not condition:
                return {'statusCode': 400, 'error': 'Missing condition'}
            columns = data.get('columns')
            if not columns:
                columns = ["*"]
            response_data = context.methods.get(
                GetPatientAppointments(
                    columns=columns,
                    condition=condition
                )
            )   
            df = response_data[0]
            if df.empty:
                return {'statusCode': 404, 'error': 'Appointment not found'}
            json_data = df.to_json()
            return {'statusCode': 200, 'message': 'GET request successful', 'data': json_data}
        except Exception as e:
            return {'statusCode': 500, 'error': 'Failed to retrieve appointment', 'message': str(e)}
    elif request.method == 'POST':
        """
        
                Create a new appointment. Requires patient_name, doctor_name, appointment_date, appointment_time, and appointment_type in the request body.
                Responds with success or failure message and the appointment_id
        """
        try:
            data = request.get_json()
            if not data: 
                return {'statusCode': 400, 'error': 'Invalid input'}
            patient_name = data.get('patient_name')
            doctor_name = data.get('doctor_name')
            patient_id = context.database.select('patients', ['patient_id'], {"=": ['patient_name', patient_name]})
            doctor_id = context.database.select('doctors', ['doctor_id'], {"=": ['doctor_name', doctor_name]})
            appointment_date = data.get('appointment_date')
            appointment_time = data.get('appointment_time')
            appointment_type = data.get('appointment_type')
            appointment_status = 'scheduled'
            patient_id = int(patient_id['patient_id'][0])
            doctor_id = int(doctor_id['doctor_id'][0])
            context.methods.create(
                CreatePatientAppointment(
                    appointment=PatientAppointment(
                        patient_name=patient_name, 
                        patient_id=patient_id,
                        doctor_id=doctor_id,
                        doctor_name=doctor_name,
                        appointment_date=appointment_date,
                        appointment_time=appointment_time,
                        appointment_type=appointment_type,
                        appointment_status=appointment_status
                    )
                )
            )
            appointment_id = context.database.select('appointments', ['appointment_id'], {"=": ['patient_id', patient_id]})
            if appointment_id.empty:
                return {'statusCode': 404, 'error': 'Appointment not found'}
            appointment_id = appointment_id['appointment_id'][0]
            return {'statusCode': 201, 'message': 'Successfully scheduled appointment', 'appointmentId': appointment_id}
        except Exception as e:
            return {'statusCode': 500, 'error': 'Failed to schedule appointment', 'message': str(e)}
    elif request.method == 'PUT':
        """
        Update an existing appointment. Requires appointment_id, patient_id, and update_data in the request body.
        Responds with success or failure message and the appointment_id
        """
        try:
            data = request.get_json()
            if not data:
                return {'statusCode': 400, 'error': 'Invalid input'}
            appointment_id = data.get('appointment_id')
            patient_id = data.get('patient_id')
            if not appointment_id:
                return {'statusCode': 400, 'error': 'Missing appointment_id'}
            if not patient_id:
                return {'statusCode': 400, 'error': 'Missing patient_id'}
            update_data = data.get('update_data')
            context.methods.update(
                UpdatePatientAppointment(
                    condition={
                            "and": [
                                {"=": ["appointment_id", appointment_id]},
                                {"=": ["patient_id", patient_id]}

                            ]
                        },
                    values_to_update=update_data
                )
            )
            return {'statusCode': 200, 'message': 'Successfully updated appointment', 'appointmentId': appointment_id}
        except Exception as e:
            return {'statusCode': 500, 'error': 'Failed to update appointment', 'message': str(e)}
    elif request.method == 'DELETE':
        """
        Delete an existing appointment. Requires appointment_id and patient_id in the request body.
        """
        try: 
            data = request.get_json()
            if not data:
                return {'statusCode': 400, 'error': 'Invalid input'}
            appointment_id = data.get('appointment_id')
            patient_id = data.get('patient_id')
            if not appointment_id:
                return {'statusCode': 400, 'error': 'Missing appointment_id'}
            if not patient_id:
                return {'statusCode': 400, 'error': 'Missing patient_id'}
            context.methods.delete(
                DeletePatientAppointment(
                    condition={
                            "and": [
                                {"=": ["appointment_id", appointment_id]},
                                {"=": ["patient_id", patient_id]}

                            ]
                        }
                )
            )
            return {'statusCode': 200, 'message': 'Successfully deleted appointment', 'appointmentId': appointment_id}
        except Exception as e:
            return {'statusCode': 500, 'error': 'Failed to update appointment', 'message': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
    serve(app, port=5000)