from ...shared.factory import Factory


def main():
    factory = Factory()
    repository = factory.create_repository()
    config = factory.create_config()
    repository.seed_products(config.products_count)
    print("Seeding products is complete, exiting...", flush=True)


if __name__ == '__main__':
    main()
