from .repository import Repository
from .config import Config
from ..services.monitor.products_client import ProductsClient
from ..services.monitor.monitor import Monitor
from .bus import Bus
from .logger import Logger


class Factory:
    def create_repository(self):
        return Repository(Config())

    def create_config(self):
        return Config()

    def create_products_client(self):
        return ProductsClient(Config(), Logger())

    def create_bus(self):
        return Bus(Config())

    def create_monitor(self):
        config = Config()
        logger = Logger(config)
        return Monitor(
            config = config, 
            repository=Repository(config), 
            client=ProductsClient(config, logger), 
            bus=Bus(config), 
            logger=logger
        )
