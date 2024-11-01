import structlog
import logging

from .config import Config


class Logger:
    def __init__(self, config: Config):
        self.config = config
        # Configure the standard logging
        logging.basicConfig(format='%(message)s', level=logging.INFO)

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.processors.KeyValueRenderer(key_order=['event', 'user_id', 'request_id'])
            ],
            context_class=dict,
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
        )
        self.logger = structlog.get_logger()
        logging.getLogger("httpx").setLevel(logging.WARNING)


    def debug(self, message, **kwargs):
        self.logger.debug(message, **kwargs)

    def info(self, message, **kwargs):
        self.logger.info(message, **kwargs)

    def warning(self, message, **kwargs):
        self.logger.warning(message, **kwargs)

    def error(self, message, **kwargs):
        self.logger.error(message, **kwargs)

    def critical(self, message, **kwargs):
        self.logger.critical(message, **kwargs)

    def exception(self, message, **kwargs):
        self.logger.exception(message, **kwargs)

    def log(self, level, message, **kwargs):
        self.logger.log(level, message, **kwargs)