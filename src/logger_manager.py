import logging
import datetime
import os

class LoggerManager:

    """
    Manages logging for the application. Logs are saved to a file named with the current date.
    This class implements the Singleton pattern to ensure only one instance exists.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):

        """
        Create a singleton instance of LoggerManager.
        """

        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialize_logger(*args, **kwargs)
        return cls._instance

    def _initialize_logger(self, log_level=logging.INFO):

        """
        Initializes the logger.

        Args:
            log_level (int): Logging level (default: logging.INFO)
        """

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self._setup_file_handler()
        self._setup_console_handler()

    def _setup_file_handler(self):

        """
        Sets up the file handler to log messages to a file with the current date.
        """

        os.makedirs('logs', exist_ok=True)

        log_filename = 'logs/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def _setup_console_handler(self):

        """
        Sets up a console handler to log messages to the standard output.
        """

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def get_logger(self):

        """
        Returns the logger instance.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        
        return self.logger
