import asyncio
import threading
from enum import Enum

from ...shared.config import Config
from ...shared.repository import Repository
from ...shared.bus import Bus
from .products_client import ProductsClient
from ...shared.logger import Logger


class MonitorState(Enum):
    STARTED = 1
    STOPPED = 0


class Monitor:
    """A class to monitor product prices asynchronously."""

    def __init__(
            self, 
            config: Config, 
            repository: Repository, 
            client: ProductsClient, 
            bus: Bus,
            logger: Logger
        ):
        self.config = config
        self.repository = repository
        self.client = client
        self.bus = bus
        self.logger = logger
        self._thread = None
        self._stop_flag = False
        self._state = MonitorState.STOPPED


    def start(self, wait=False):
        self._thread = threading.Thread(target=self._update_prices_async)
        self._thread.start()
        self._state = MonitorState.STARTED
        if wait:
            self._thread.join()


    def stop(self):
        self._stop_flag = True
        if self._thread:
            self._thread.join()  # wait for the thread to finish
        self._state = MonitorState.STOPPED



    def _update_prices_async(self):
        asyncio.run(self._update_prices())
        

    async def _update_prices(self):
        self.logger.info("monitor service started")
        
        while not self._stop_flag:
            await self._process_batch()
        
        self.logger.info("monitor service stopped")


    async def _process_batch(self):
        try:
            self.logger.debug("start processing new batch ...")
            product_ids = self.repository.lock_least_updated_products(self.config.batch_size)
            products = await self.client.get_products_data(product_ids)
            self.bus.publish_product_prices(products)
            self.repository.update_unlock_products(product_ids)
            self.logger.debug(f"finished processing batch of {len(product_ids)} products")
        
        except Exception as e:
            ## on error, unlocks products without updating last access time
            self.repository.unlock_products(product_ids)
            self.logger.exception('unexpected error occured while processing batch of products', product_ids)

    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
