from auth.authorizor import Auth
from auth.session_manager import SessionManager

class ContextHSM:
    def __init__(self):
        self.authenticator = Auth()
        self.get_session_manager()

    def get_context(self):
        pass

    def get_session_manager(self):
        self.session_manager = SessionManager()

