import os
import logging


class Config:

    @property
    def products_service_url(self):
        return os.getenv('PRODUCTS_SERVICE_URL', 'http://fake-products:5000')

    @property
    def redis_host(self):
        return os.getenv('REDIS_HOST', 'redis')

    @property
    def redis_port(self):
        return int(os.getenv('REDIS_PORT', 6379))

    @property
    def redis_password(self):
        return os.getenv('REDIS_PASSWORD', None)  # No password by default

    @property
    def redis_db(self):
        return int(os.getenv('REDIS_DB', 0))  # Default to DB 0

    @property
    def batch_size(self):
        return int(os.getenv('BATCH_SIZE', 50))

    @property
    def products_count(self):
        return int(os.getenv('PRODUCTS_COUNT', 1000))

    @property
    def loglevel(self):
        return self._parse_log_level(os.getenv('LOGLEVEL', 'INFO'))

    def _parse_log_level(self, level_str):
        level_str = level_str.upper()  # Make it case-insensitive
        if level_str in logging._nameToLevel:
            return logging._nameToLevel[level_str]  # Get the corresponding numeric level
        else:
            raise ValueError(f"'{level_str}' is not a valid logging level.")

    def __repr__(self):
        properties = {key: getattr(self, key) for key in dir(self) if isinstance(getattr(self.__class__, key), property)}
        return f"Config({', '.join(f'{k}={v!r}' for k, v in properties.items())})"
