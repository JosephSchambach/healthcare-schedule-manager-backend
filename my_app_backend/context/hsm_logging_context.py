import logging

class LoggingContext:
    def __init__(self, logger_name: str = 'my_app_logger'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

    def log(self, message: str, level: str = 'info'):
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        else:
            self.logger.info(message)
