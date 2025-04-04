from hsm_auth.authorizor import Auth
from hsm_auth.session_manager import SessionManager
from hsm_database.database_config import DataBaseConfig
import json

class ContextHSM:
    def __init__(self):
        self.authenticator = Auth()
        self.get_session_manager()
        self.get_context()
        self.get_secrets()
        self.get_database()

    def get_context(self):
        with open('my_app_backend/context/config.json') as json_file:
            data = json.load(json_file)
            if data["context"] == "HSM": 
                self.context = data
        json_file.close()

    def get_secrets(self):
        secrets = self.context.get("secrets")
        if secrets:
            self.secrets = secrets
        else:
            raise ValueError("Secrets not found in context configuration")

    def get_session_manager(self):
        self.session_manager = SessionManager()

    def get_database(self):
        database = self.secrets.get("database")
        if database:
            self.database = DataBaseConfig(database)
        else:
            raise ValueError("Database not found in secrets configuration")

