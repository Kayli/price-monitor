import redis
import json

from ..services.monitor.products_client import ProductData
from .config import Config


class Bus:
    def __init__(self, config: Config):
        self.config = config
        self.redis = redis.Redis(
            host=self.config.redis_host,
            port=self.config.redis_port,
            password=self.config.redis_password,
            db=self.config.redis_db
        )
        self.price_channel = "price_updates"


    def publish_product_prices(self, products: list[ProductData]):
        # Convert the list of prices to a JSON string
        products_json = json.dumps([product.model_dump_json() for product in products], indent=2)
        
        # Publish the JSON string to the price_updates channel
        self.redis.publish(self.price_channel, products_json)


    def subscribe_to_prices(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.price_channel)
        for message in pubsub.listen():
            if message['type'] != 'message':
                continue
            json_string = message['data'].decode('utf-8')
            products_data = json.loads(json_string)
            for product in products_data:
                yield product
