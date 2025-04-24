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

    def select(self, table_name: str, columns: list, condition: str = None):
        self.logger.log(f"Selecting data from: {table_name}")
        self.database.select(table_name, columns, condition)

    def insert(self, table_name: str, columns: list, data: list | dict | tuple):
        self.logger.log(f"Inserting data into table: {table_name}")
        if data is None:
            raise ValueError("Data cannot be None")
        try:
            if isinstance(data, tuple):
                data = [value for value in data]
            else:
                raise ValueError("Data must be a DataFrame or a dictionary")
            self.database.insert(table_name, columns, data)
            self.logger.log("Data inserted successfully")
        except Exception as e:
            self.logger.log(f"Error inserting data: {e}", 'error')
            raise e

    def update(self, query: str, data: dict, condition: str = None):
        pass