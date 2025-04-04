from hsm_database.supabase_config import SupabaseConfig
import pandas as pd

class DataBaseConfig:
    def __init__(self, auth_config: dict):
        if not auth_config:
            raise ValueError("Auth configuration is required")
        self._setup_database(auth_config)

    def _setup_database(self, auth_config: dict):
        if 'supabase' in auth_config:
            self.database = SupabaseConfig(auth_config['supabase'])

    def query(self, query: str):
        pass

    def insert(self, table: str, data: dict):
        pass

    def update(self, table: str, data: dict, condition: str):
        pass