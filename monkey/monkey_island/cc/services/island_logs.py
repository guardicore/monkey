import logging

__author__ = "Maor.Rayzin"

logger = logging.getLogger(__name__)


class IslandLogService:
    def __init__(self):
        pass

    @staticmethod
    def get_log_file():
        """
        This static function is a helper function for the monkey island log download function.
        It finds the logger handlers and checks if one of them is a fileHandler of any kind by checking if the handler
        has the property handler.baseFilename.
        :return:
        a dict with the log file content.
        """
        logger_handlers = logger.parent.handlers
        for handler in logger_handlers:
            if hasattr(handler, 'baseFilename'):
                logger.info('Log file found: {0}'.format(handler.baseFilename))
                log_file_path = handler.baseFilename
                with open(log_file_path, 'rt') as f:
                    log_file = f.read()
                return {
                    'log_file': log_file
                }

        logger.warning('No log file could be found, check logger config.')
        return None
