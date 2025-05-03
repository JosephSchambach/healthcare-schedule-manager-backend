from my_app_backend.hsm_models.custom_models import get_obj_config
from time import sleep

class Methods:
    def __init__(self, logger, database=None):
        self.logger = logger
        self.database = database
        self.object_config = get_obj_config()
        
    def create(self, args, log=True, alert=None):
        arg_type = type(args)
        create_response = []
        if log:
            self.logger.log(f"Creating object of type {arg_type}")
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Processing {i+1} {arg_type} objects")
            kwargs = self.object_config[arg.__class__.__name__]
            result = self._process(arg, kwargs, alert=alert)
            if result is not None:
                actor = getattr(self, result["context_method"])
                action = getattr(actor, result["execution_method"])
                action_response = action(result["table"], result["columns"], result["values"])
                create_response.append(action_response)
        if log:
            self.logger.log(f"Created {len(create_response)} objects of type {arg_type}")
        return create_response
        
    def update(self, args, log: bool =True, alert: bool = None):
        arg_type = type(args)
        update_response = []
        if log:
            self.logger.log(f"Updating object of type {arg_type}")
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Processing {i + 1} {arg_type} objects")
            kwargs = self.object_config[arg.__class__.__name__]
            result = self._process(arg, kwargs, alert=alert)
            if result is not None:
                actor = getattr(self, result["context_method"])
                action = getattr(actor, result["execution_method"])
                action_response = action(result["table"], result["columns"], result["values"], result["condition"])
                update_response.append(action_response)
        if log:
            self.logger.log(f"Updated {len(update_response)} objects of type {arg_type}")
        return update_response
        
    def delete(self, args, log: bool =True, alert: bool = None):
        arg_type = type(args)
        delete_response = []
        if log: 
            self.logger.log(f"Deleting object of type {arg_type}")

    def lookup(self, args, log: bool =True, alert: bool = None):
        arg_type = type(args)
        lookup_response = []
        if log:
            self.logger.log(f"Looking up object of type {arg_type}")
            
    def _process(self, args, kwargs, log = None, alert = None, retries = 0, retry_interval = 0):
        for _ in range(retries + 1):
            try:
                parent_method = kwargs.get("parent_method")
                kwargs = kwargs.get("kwargs", {})
                if log:
                    self.logger.log(f"Processing {args} with parent method {parent_method}")
                return parent_method(args, **kwargs)
            except Exception as e:
                if log: 
                    self.logger.error(f"Error processing {args}: {e}")
                if _ == retries - 1:
                    if alert:
                        self.logger.alert(f"Failed to process {args} after {retries} retries")
                    raise e
                sleep(retry_interval)
                continue