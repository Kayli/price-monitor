# Price Monitor

Price Monitor is a Python-based tool designed to track and monitor product prices from various e-commerce websites. The application allows users to receive alerts whenever the price of an item drops below a specified threshold, making it an ideal solution for users looking to save money on online purchases.

## Warning

This is a code for a time-boxed implementation of a take-at-home test project!

## Features

- Automated Price Tracking: Automatically tracks prices on specified e-commerce websites
- Asynchronous Execution: Optimized for performance with asynchronous requests.
- Horizontal scaling: Supports manual scaling by simply increasing number of monitor component instances (see docker-compose.yaml)
- Easy Setup: Minimal configuration required for getting started


## Getting Started

### Prerequesites

Make sure git, docker-compose and poetry are installed.

### Instructrions

Clone repository
```bash
git clone https://github.com/Kayli/price-monitor.git
cd price-monitor
```

Run project using docker-compose orchestrator
```bash
docker compose -f infrastructure/docker-compose.yml up
```

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


## How to run in a cloud environment

To run the application in a cloud environment using Kubernetes:

- Choose a Cloud Provider: Use a Kubernetes-supported cloud service (e.g., Google Kubernetes Engine (GKE), Amazon EKS, or Azure AKS).

- Set Up Docker Registry: Push your Docker images to a container registry (e.g., Docker Hub, AWS ECR, or Google Container Registry).

- Provision Kubernetes Cluster: Create a Kubernetes cluster on your cloud provider, configuring node pools, networking, and storage as needed.

- Convert Docker Compose to Kubernetes Manifests: Use tools like kompose to convert your Docker Compose files to Kubernetes YAML manifests, or manually create Deployment, Service, and ConfigMap/Secret files.

- Deploy to Cluster: Use kubectl apply to deploy your Kubernetes manifests to the cluster.

- Configure Environment Variables and Secrets: Define environment variables and store sensitive data in Kubernetes Secrets.

- Expose and Monitor: Set up Services and Ingress for public access, configure scaling and monitoring through Kubernetes tools or your cloud provider.

This will deploy your Docker Compose stack as a Kubernetes application in the cloud.

## Known problems

- If any error occurs during remote api call
    - monitor component will discard the whole batch of async requests, which is somewhat wasteful
    - monitor component will retry to update price again and again until it succeeds, so there is no protection against 'poisoned' product urls
- Only monitor is covered with unit tests, but there are no automated integration tests for the application
- There is no coverage metrics collected during tests run
- There is no automated performance testing implemented
- There is no automated security scanning implemented
- There is no ci/cd pipeline configured for github repository
