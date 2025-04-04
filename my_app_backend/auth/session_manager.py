import uuid
import base64

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, auth: str):
        username = self._decode_hash(auth)
        if not username:
            return "Invalid authentication data"
        session_token = self._generate_session_token(username)
        self.sessions[session_token] = username 
        return session_token
    
    def _decode_hash(self, auth: str):
        try:
            decoded_auth = base64.b64decode(auth).decode('utf-8')
            username, password, role = decoded_auth.split(':')
            return username
        except Exception as e:
            raise ValueError(f"Failed to decode authentication: {e}")

    def _generate_session_token(self, user_id: str) -> str:
        return str(uuid.uuid4()) + user_id
    
    def delete_session(self, session_token: str):
        if session_token in self.sessions:
            del self.sessions[session_token]
        else:
            return "Session token not found"
        return "Session deleted successfully"