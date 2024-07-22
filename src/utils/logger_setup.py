import logging

class AppLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=format)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)


loggerCursor = AppLogger('MoviesLogger')
loggerCursor.info('Logger initialized')

