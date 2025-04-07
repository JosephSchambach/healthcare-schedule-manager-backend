import base64
import pandas as pd

class LoginHandler:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database

    def _decode_auth(self):
        try:
            self.__decoded_auth = base64.b64decode(self.__auth).decode('utf-8')
            self.__username, self.__password, self.__role = self.__decoded_auth.split(':')
        except Exception as e:
            raise ValueError(f"Failed to decode authentication: {e}")

    def _authenticate(self):
        data_response = pd.read_csv('my_app_backend/auth/login.csv', header='infer')
        record = data_response[(data_response['username'] == self.__username) & (data_response['role'] == self.__role)]
        if record.empty:
            return False, "Invalid username or role"
        if record.iloc[0]['password'] != self.__password:
            return False, "Invalid password"
        return True, "Authenticated successfully"
    
    def authenticate(self, auth):
        self.__auth = auth
        self._decode_auth()
        return self._authenticate()
    
    def create(self, user_model):
        self.logger.log("Creating user authentication record")
        try:
            self.database.insert(
                f"insert into user_authentication_table (username, password, role) values ('%s', '%s', '%s')", 
                (user_model.username, user_model.password, user_model.role)
            )
            self.logger.log("User authentication record created successfully")
            return True, "User authentication record created successfully"
        except Exception as e:
            self.logger.log(f"Failed to create user authentication record: {e}", level='error')
            return False, "Failed to create user authentication record"