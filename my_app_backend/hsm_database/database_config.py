from hsm_database.supabase_config import SupabaseConfig
import pandas as pd

class DataBaseConfig:
    def __init__(self, logger, auth_config: dict):
        self.logger = logger
        if not auth_config:
            raise ValueError("Auth configuration is required")
        self._setup_database(auth_config)

    def _setup_database(self, auth_config: dict):
        if 'supabase' in auth_config:
            self.database = SupabaseConfig(auth_config['supabase'])

    def query(self, query: str, condition: str = None):
        pass

    def insert(self, query: str, data):
        self.logger.log(f"Inserting data with query: {query}")
        if data is None:
            raise ValueError("Data cannot be None")
        try:
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')
            elif isinstance(data, dict):
                data = [data]
            elif isinstance(data, tuple):
                data = [value for value in data]
            else:
                raise ValueError("Data must be a DataFrame or a dictionary")
            self.database.insert(query, data)
            self.logger.log("Data inserted successfully")
        except Exception as e:
            self.logger.log(f"Error inserting data: {e}", 'error')
            raise e

    def update(self, query: str, data: dict, condition: str = None):
        pass