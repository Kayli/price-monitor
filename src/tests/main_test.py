import asyncio
from unittest.mock import AsyncMock

from ..services.monitor.monitor import Monitor, MonitorState
from .fake_factory import FakeFactory


def create_monitor():
    factory = FakeFactory()
    return factory.create_monitor()


def test_start_initializes_monitor():
    with create_monitor() as monitor:
        monitor.start()
        assert monitor._state == MonitorState.STARTED


def test_stop_stops_monitor():
    with create_monitor() as monitor:
        monitor.start() 
        monitor.stop()
        assert monitor._state == MonitorState.STOPPED


def test_process_batch_processes_products_correctly():
    with create_monitor() as monitor:
        # Set up expected product ids and product data
        monitor.repository.lock_least_updated_products.return_value = [1, 2]
        monitor.client.get_products_data = AsyncMock(
            return_value=[{"id": 1, "price": 100}, {"id": 2, "price": 200}]
        )

        # Call the _process_batch method directly
        asyncio.run(monitor._process_batch())

        monitor.repository.lock_least_updated_products.assert_called_once_with(monitor.config.batch_size)
        monitor.client.get_products_data.assert_awaited_once_with([1, 2])
        monitor.bus.publish_product_prices.assert_called_once_with([
            {"id": 1, "price": 100},
            {"id": 2, "price": 200},
        ])
        monitor.repository.update_unlock_products.assert_called_once_with([1, 2])


def test_process_batch_handles_exception_and_unlocks_products():
    with create_monitor() as monitor:
        # Simulate an error in get_products_data
        monitor.client.get_products_data = AsyncMock(side_effect=Exception("test exception"))
        monitor.repository.lock_least_updated_products.return_value = [1, 2]

        # Call the _process_batch method directly
        asyncio.run(monitor._process_batch())

        monitor.logger.exception.assert_called_with(
            "unexpected error occured while processing batch of products", [1, 2]
        )
        monitor.repository.unlock_products.assert_called_once_with([1, 2])
