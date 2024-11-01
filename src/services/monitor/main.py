import signal

from ...shared.factory import Factory


def register_graceful_termination_handler(monitor):
    def signal_handler(sig, frame):
        print("SIGTERM received. Setting flag to stop.", flush=True)
        monitor.stop()
    signal.signal(signal.SIGTERM, signal_handler)


def main():
    monitor = Factory().create_monitor()
    register_graceful_termination_handler(monitor)
    monitor.start(wait=True)


if __name__ == '__main__':
    main()
