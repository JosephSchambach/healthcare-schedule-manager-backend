from supabase import create_client, Client
import pandas as pd
import regex as re

class SupabaseConfig:
    def __init__(self, auth_dict: dict):
        self.url = auth_dict.get("supabase_url")
        self.key = auth_dict.get("supabase_key")
        self.service_role = auth_dict.get("supabase_service_role")
        self.client: Client = create_client(self.url, self.service_role)
        
    def insert(self, query: str, data: list | dict | pd.DataFrame):
        table_name = query.split(" ")[2]
        match = re.search(r'\((.*?)\)', query)
        if match:
            extracted_data = match.group(1)
        else:
            extracted_data = None
        if extracted_data:
            insert_data = {}
            columns = extracted_data.split(",")
            for i in range(len(columns)):
                insert_data[columns[i].strip()] = data[i]
        try:
            self.client.table(table_name).insert(insert_data).execute()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise e