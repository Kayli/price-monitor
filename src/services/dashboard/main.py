import time
import threading
import signal
import asyncio
from ...shared.factory import Factory


def subscribe_and_update(bus, update_count, lock):
    for product in bus.subscribe_to_prices():
        with lock:  # Acquire the lock before updating the count
            update_count[0] += 1  # Increment the update count


def signal_handler(sig, frame):
    """Signal handler for SIGTERM"""
    print("SIGTERM received. Setting flag to stop.", flush=True)
    loop = asyncio.get_event_loop()
    loop.stop()
    loop.close()


async def main():
    signal.signal(signal.SIGTERM, signal_handler)

    bus = Factory().create_bus()

    print("dashboard service started!", flush=True)

    update_count = [0]
    lock = threading.Lock()  # Lock to ensure thread-safe access to update_count

    # Start a separate thread for subscribing to price updates
    subscription_thread = threading.Thread(target=subscribe_and_update, args=(bus, update_count, lock), daemon=True)
    subscription_thread.start()

    # Print the update count every sample_time seconds in the main thread
    while True:
        sample_time = 5
        time.sleep(sample_time)
        with lock:  # Acquire the lock to read the update count safely
            print(f"Number of price updates in the last {sample_time} seconds: {update_count[0]}", flush=True)
            update_count[0] = 0  # Reset the counter after printing


if __name__ == '__main__':
    asyncio.run(main())
