from my_app_backend.hsm_database.supabase_config import SupabaseConfig
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
        data = self.database.select(table_name, columns, condition)
        if data.empty:
            self.logger.log("No data found", 'warning')
            return pd.DataFrame()
        self.logger.log("Data selected successfully")
        return data

    def insert(self, table_name: str, columns: list, data: list | dict | tuple):
        self.logger.log(f"Inserting data into table: {table_name}")
        if data is None:
            raise ValueError("Data cannot be None")
        try:
            if isinstance(data, tuple):
                data = [value for value in data]
            # else:
            #     raise ValueError("Data must be a DataFrame or a dictionary")
            self.database.insert(table_name, columns, data)
            self.logger.log("Data inserted successfully")
        except Exception as e:
            self.logger.log(f"Error inserting data: {e}", 'error')
            raise e

    def update(self, table_name: str, columns: list, data: list, condition: str = None):
        self.logger.log(f"Updating data in table: {table_name}")
        if not data:
            raise ValueError("Data cannot be empty")
        try:
            self.database.update(table_name, columns, data, condition)
            self.logger.log("Data updated successfully")
        except Exception as e:
            self.logger.log(f"Error updating data: {e}", 'error')
            raise e
        
    def delete(self, table_name: str, condition: str = None):
        self.logger.log(f"Deleting data from table: {table_name}")
        try:
            self.database.delete(table_name, condition)
            self.logger.log("Data deleted successfully")
        except Exception as e:
            self.logger.log(f"Error deleting data: {e}", 'error')
            raise e