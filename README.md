# Price Monitor

Price Monitor is a Python-based tool designed to track and monitor product prices from various e-commerce websites. The application allows users to receive alerts whenever the price of an item drops below a specified threshold, making it an ideal solution for users looking to save money on online purchases.

## Features

- Automated Price Tracking: Automatically tracks prices on specified e-commerce websites
- Asynchronous Execution: Optimized for performance with asynchronous requests.
- Horizontal scaling: Supports manual scaling by simply increasing number of monitor component instances
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
