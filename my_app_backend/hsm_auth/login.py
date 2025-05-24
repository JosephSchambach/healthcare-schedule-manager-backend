import base64
import pandas as pd

class LoginHandler:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self.__table_maps = {
            'patient': ['patients', 'patient_name'],
            'doctor': ['doctors', 'doctor_name'],
            'admin': ['admins', 'admin_name']
        }

    def _decode_auth(self):
        try:
            self.__decoded_auth = base64.b64decode(self.__auth).decode('utf-8')
            self.__username, self.__password, self.__role = self.__decoded_auth.split(':')
        except Exception as e:
            raise ValueError(f"Failed to decode authentication: {e}")

    def _authenticate(self):
        record = self.database.select(
            "user_authentication_table",
            "*",
            {
                "and": [
                    {
                        "=":
                        ["username", self.__username]
                    },
                    {
                        "=":
                        ["role", self.__role]
                    },
                    {
                        "=":
                        ["password", self.__password]
                    }
                ]
            }
        )
        if record.empty:
            return False, "Invalid username or role"
        return True, "Authenticated successfully", record.to_dict(orient='records')[0]['unique_id']
    
    def authenticate(self, auth):
        self.__auth = auth
        self._decode_auth()
        return self._authenticate()
    
    def create(self, user_model, name):
        self.logger.log("Creating user authentication record")
        try:
            self.database.insert(
                'user_authentication_table', ['username', 'password', 'role'], 
                (user_model['username'], user_model['password'], user_model['role'],)
            )
            self.logger.log("User authentication record created successfully")
            table_name = self.__table_maps.get(user_model['role'])[0]
            column_name = [self.__table_maps.get(user_model['role'])[1]]
            self.database.insert(
                table_name, column_name,
                (name,)
            )
            return True, "User authentication record created successfully"
        except Exception as e:
            self.logger.log(f"Failed to create user authentication record: {e}", level='error')
            return False, "Failed to create user authentication record"