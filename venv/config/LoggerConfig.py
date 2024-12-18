import logging

class LoggerConfig:

    @staticmethod
    def configure_logger():
        logger = logging.getLogger("uvicorn")
        logger.setLevel(logging.INFO)
        return logger

logger = LoggerConfig.configure_logger()