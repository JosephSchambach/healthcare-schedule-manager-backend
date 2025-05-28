from uuid import uuid4

def _generate_id():
    return str(uuid4())

class AppointmentHandler:
    def __init__(self, database):
        self.database = database
        self.scheduled = False
    
    def schedule(self, attribute, context_method, execution_method):
        appointment = getattr(self, attribute)
        appointment_id = _generate_id()
        data = vars(appointment)
        data['appointment_id'] = appointment_id
        data['appointment_status'] = 'scheduled'
        columns = list(data.keys())
        values = list(data.values())
        return {"table": "appointments", "columns": columns, "values": values, "context_method": context_method, "execution_method": execution_method}
    
    def reschedule(self, attribute, update_data, context_method, execution_method):
        condition = getattr(self, attribute)
        update_dict = getattr(self, update_data)
        columns, values = [], []
        for key, value in update_dict.items():
            columns.append(key)
            values.append(value)
        return {"table": "appointments", "columns": columns, "values": values, "condition": condition, "context_method": context_method, "execution_method": execution_method}
    
    def cancel(self, attribute, update_data, context_method, execution_method):
        condition = getattr(self, attribute)
        update_value = getattr(self, update_data)
        return {"table": "appointments", "columns": update_data, "values": update_value, "condition": condition, "context_method": context_method, "execution_method": execution_method}
    
    def get(self, attribute, data, context_method, execution_method):
        condition = getattr(self, attribute)
        columns = getattr(self, data)
        return {"table": "appointments", "columns": columns, "condition": condition, "context_method": context_method, "execution_method": execution_method}