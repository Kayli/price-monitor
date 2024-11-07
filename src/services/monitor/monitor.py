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
            logger: Logger):
        self._config = config
        self._repository = repository
        self._client = client
        self._bus = bus
        self._logger = logger
        self._thread = None
        self._stop_flag = False
        self._state = MonitorState.STOPPED

    @property
    def state(self):
        return self._state

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
        self._logger.info("monitor service started")

        while not self._stop_flag:
            await self._process_batch()

        self._logger.info("monitor service stopped")

    async def _process_batch(self):
        try:
            self._logger.debug("start processing new batch ...")
            product_ids = self._repository.lock_least_updated_products(self._config.batch_size)
            products = await self._client.get_products_data(product_ids)
            self._bus.publish_product_prices(products)
            self._repository.update_unlock_products(product_ids)
            self._logger.debug(f"finished processing batch of {len(product_ids)} products")

        except Exception:
            ## on error, unlocks products without updating last access time
            self._repository.unlock_products(product_ids)
            self._logger.exception('unexpected error occured while processing batch of products', product_ids)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
