from typing import Optional, Dict, List, Tuple, Any

class QueryFactory:
    def __init__(self, query: str, condition: dict = None, data: Optional[dict | List | Tuple | Any] = None):
        self.query = query
        self.condition = condition
        self.data = data

    def create_query(self) -> str:
        """
        Create a query based on the provided query string and condition.
        """
        if self.condition:
            condition_str = "where " + self._condition_handler(self.condition)
            return f"{self.query} {condition_str}"
        return self.query
    
    def _condition_constructor(self, condition) -> str:
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
        def handle_and(conditions):
            condition_string = ""
            for cond in conditions:
                if isinstance(cond, dict):
                    value = self._condition_handler(cond)
                    if value and 'and' in condition_string:
                        condition_string += value
                    elif value:
                        condition_string += value + " and "
                    else:
                        condition_string += ""
            return f"({condition_string})"
        def handle_or(conditions):
            condition_str = ""
            for cond in conditions:
                if isinstance(cond, dict):
                    value = self._condition_handler(cond)
                    if value and 'or' in condition_str:
                        condition_str += value
                    elif value:
                        condition_str += value + " or "
                    else:
                        condition_str += ""
            return f"({condition_str})"
        if not condition:
            return ""
        for key, value in condition.items():
            if key == "and": 
                condition_str += handle_and(value)
            elif key == "or": 
                condition_str += handle_or(value)
            else: 
                column, value = value
                condition_str += f"{column} {key} '{value}'"
        return condition_str
    
    def _condition_handler(self, query: dict, supabase: )