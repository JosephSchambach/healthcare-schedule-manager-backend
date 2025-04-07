from hsm_auth.login import LoginHandler
from hsm_auth.session_manager import SessionManager
from hsm_database.database_config import DataBaseConfig
from context.hsm_logging_context import LoggingContext
import json

class ContextHSM:
    def __init__(self):
        self.logger = LoggingContext()
        self.get_session_manager()
        self.get_context()
        self.get_secrets()
        self.get_database()
        self.login = LoginHandler(self.logger, self.database)

    def get_context(self):
        with open('context_config.json') as json_file:
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
            self.database = DataBaseConfig(self.logger, database)
        else:
            raise ValueError("Database not found in secrets configuration")

