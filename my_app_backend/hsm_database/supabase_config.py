from supabase import create_client, Client
import pandas as pd
import regex as re

class SupabaseConfig:
    def __init__(self, auth_dict: dict):
        self.url = auth_dict.get("supabase_url")
        self.key = auth_dict.get("supabase_key")
        self.service_role = auth_dict.get("supabase_service_role")
        self.client: Client = create_client(self.url, self.service_role)
        
    def insert(self, table_name: str, columns: list, data: list | dict):
        def _row_builder(columns, data):
            rows = []
            row = {}
            if isinstance(data, dict):
                data = list(data.values())
            while len(data) > 0:
                for i in range(len(columns)):
                    if len(data) > 0:
                        row[columns[i].strip()] = data[0]
                        data = data[1:]
                rows.append(row)
            return rows
        
        insert_data = {}
        if len(columns) != len(data):
            insert_data = _row_builder(columns, data)
        else:
            for i in range(len(columns)):
                insert_data[columns[i].strip()] = data[i]
        try:
            self.client.table(table_name).insert(insert_data).execute()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise e
        
    def select(self, table_name: str, columns: str, condition: dict = None):
        query = self.client.table(table_name).select(columns)
        if condition is not None:
            query = self._condition_handler(query, condition)
        try:
            response = query.execute()
            if response.data is None:
                return pd.DataFrame()
            if isinstance(response.data, list):
                return pd.DataFrame(response.data)
            else:
                return pd.DataFrame([response.data])
        except Exception as e:
            print(f"Error selecting data: {e}")
            raise e
            

    def _condition_parser(self, condition: str):
        """
            This would be a normal where clause in sql. 
            Example: where column_name = value and column_name = value or column_name = value
        """

    def _condition_handler(self, supabase, condition: dict, query: str = None, is_or: bool = False):
        """
            basic format of condition is:
                {
                    "and": [
                        {
                            "=": ["column_name", "value"]
                        },
                        {
                            ">": ["column_name", "value"]
                        }
                    ]
                }
        """
        if condition is None and query is None:
            return supabase
        if condition is not None:
            for key, value in condition.items():
                if key == 'and': 
                    for sub_condition in value:
                        supabase = self._condition_handler(supabase, sub_condition)
                elif key == 'or': 
                    or_string = ""
                    for i, sub_condition in enumerate(value):
                        or_string += f"{self._condition_handler(supabase, sub_condition, is_or=True)}"
                        if i < len(value) - 1:
                            or_string += ","
                    supabase = supabase.or_(or_string)
                else:
                    column = value[0].strip()
                    if len(value[1].split(",")) > 1:
                        value = value[1].split(",")
                        value = [v.strip() for v in value]
                    else:
                        value = value[1].strip()
                    if key == '=':
                        if is_or:
                            return f"{column}.eq.{value}"
                        else:
                            return supabase.eq(column, value)
                    elif key == '!=':
                        if is_or:
                            return f"{column}.neq.{value}"
                        else:
                            return supabase.neq(column, value)
                    elif key == '>':
                        if is_or:
                            return f"{column}.gt.{value}"
                        else:
                            return supabase.gt(column, value)
                    elif key == '<':
                        if is_or:
                            return f"{column}.lt.{value}"
                        else:
                            return supabase.lt(column, value)
                    elif key == 'like':
                        if is_or:
                            return f"{column}.ilike.{value}"
                        else:
                            return supabase.ilike(column, f"%{value}%")
                    elif key == 'in':
                        value = ','.join(value)
                        if is_or:
                            return f"{column}.in.({value})"
                        else:
                            return supabase.in_(column, value)
                    elif key == 'not in':
                        value = ','.join(value)
                        if is_or:
                            return f"{column}.not.in.({value})"
                        else:
                            return supabase.not_.in_(column, f"({value})")
                    elif key == 'is':
                        if is_or:
                            return f"{column}.is.{value}"
                        else:
                            return supabase.is_(column, value)
                    elif key == 'is not':
                        if is_or:
                            return f"{column}.is.not.{value}"
                        else:
                            return supabase.is_not(column, value)
                    else:
                        raise ValueError(f"Unsupported operator: {key}")
        return supabase