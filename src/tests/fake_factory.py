from unittest.mock import Mock

from ..shared.repository import Repository
from ..shared.config import Config
from ..shared.bus import Bus
from ..shared.logger import Logger
from ..services.monitor.products_client import ProductsClient
from ..services.monitor.monitor import Monitor


class FakeFactory:
    """Creates an instance of a Monitor with mocked dependencies"""

    def create_monitor(self):
        # Create mock instances for each dependency
        config = Mock(spec=Config)
        config.batch_size = 10  # Provide any other necessary attributes for testing

        logger = Mock(spec=Logger)
        
        # Create mock instances for Repository, ProductsClient, and Bus
        repository = Mock(spec=Repository)
        repository.lock_least_updated_products.return_value = [1, 2]
        
        client = Mock(spec=ProductsClient)
        client.get_products_data.return_value = [
            {"id": 1, "price": 100},
            {"id": 2, "price": 200},
        ]
        
        bus = Mock(spec=Bus)
        
        # Return a Monitor instance using mock dependencies
        return Monitor(
            config=config,
            repository=repository,
            client=client,
            bus=bus,
            logger=logger
        )
