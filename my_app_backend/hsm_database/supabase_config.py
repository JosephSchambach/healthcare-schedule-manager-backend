from supabase import create_client, Client
import pandas as pd

class SupabaseConfig:
    def __init__(self, auth_dict: dict):
        self.url = auth_dict.get("supabase_url")
        self.key = auth_dict.get("supabase_key")
        self.service_role = auth_dict.get("supabase_service_role")
        self.client: Client = create_client(self.url, self.service_role)