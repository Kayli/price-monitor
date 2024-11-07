# Price Monitor

Price Monitor is a Python-based tool designed to track and monitor product prices from various e-commerce websites. The application allows users to receive alerts whenever the price of an item drops below a specified threshold, making it an ideal solution for users looking to save money on online purchases.


## Features

- Automated Price Tracking: Automatically tracks prices on specified e-commerce websites
- Asynchronous Execution: Optimized for performance with asynchronous requests.
- Horizontal scaling: Supports manual scaling by simply increasing number of monitor component instances (see docker-compose.yaml)
- Easy Setup: Minimal configuration required for getting started


## Getting Started

Clone repository
```bash
git clone https://github.com/Kayli/price-monitor.git
```
Make sure docker is installed.

Run project using docker-compose orchestrator
```bash
cd infrastructure
docker compose up
```
Make sure poetry is installed.

Run tests
```bash
poetry install --with dev
poetry run pytest
```

## Key components

### Services

- src/services/monitor: a scalable 'agent' component encapsulating high-level business logic
- src/services/fake_products: fake  service that emulates api with ever-changing prices
- src/services/init: init container that is used to seed product ids into a redis cache
- src/services/dashboard: barebones terminal-based dashboard that simply prints out number messages recieved over the last X minutes
- redis
    - helps with caching product ids we have to monitor
    - serves as distibuted locking mechanism, coordinating and splitting work among multiple 'monitor' instances
    - used as message bus to pass price updates asynchronously to the dashboard service


### Shared modules/classes

- ProductsClient: encapsulates API interactions with fake_products service
- Bus: encapsulates message bus functionality implemented by redis
- Config: encapsulates application configuration that, which values can be overriden by environment variables
- Factory: encapsulates creation of the application components following a factory design pattern. Performs dependency injection.
- Logger: encapsulates structural logger component interface and its configuration
- Repository: encapsulates interactions and configuration of cache storage used for caching product ids that we have to monitor. Contains distributed locking logic that enables monitoring of multiple product prices in a horizontally scalable manner.


## Known problems

- if any error occurs during remote api call
    - monitor component will discard the whole batch of async requests, which is somewhat wasteful
    - monitor component will retry to update price again and again until it succeeds, so there is no protection against 'poisoned' product urls
- only monitor is covered with unit tests, but there are no automated integration tests for the application
- there is no coverage metrics collected during tests run
- there is no automated performance testing implemented
- there is no automated security scanning implemented
- there is no ci/cd pipeline configured for github repository