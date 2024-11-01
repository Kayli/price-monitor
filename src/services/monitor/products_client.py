import httpx
import asyncio
import json
from pydantic import BaseModel, ValidationError

from ...shared.config import Config
from ...shared.logger import Logger


class ProductData(BaseModel):
    id: int
    name: str
    price: float


class ProductsClient:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.timeout = httpx.Timeout(
            connect=10.0,  # 10 seconds to connect
            read=30.0,     # 30 seconds to read response
            write=30.0,    # 30 seconds to write request
            pool=10.0      # 10 seconds to wait for a connection from the pool
        )
    

    async def get_products_data(self, ids) -> list[ProductData]:
        results = []
        urls = [f"{self.config.products_service_url}/products/{i + 1}" for i in ids]
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = [self._fetch(client, url) for url in urls]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

        return results


    # Function to fetch a single URL
    async def _fetch(self, client, url) -> ProductData:
        self.logger.debug(f"fetching url {url} ...")
        response = await client.get(url)
        return ProductData.model_validate_json(response.text)
