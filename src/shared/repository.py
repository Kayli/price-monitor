import redis
import time

from .config import Config


class Repository:
    def __init__(self, config: Config):
        self.config = config
        self.redis = redis.Redis(
            host=self.config.redis_host,
            port=self.config.redis_port,
            password=self.config.redis_password,
            db=self.config.redis_db
        )
        self.products_key = "products:last_updated"
        self.lock_key_prefix = "lock:product:"


    def seed_products(self, target_count: int):
        # Initialize products with a timestamp of 0 (Unix epoch start time)
        initial_timestamp = 0
        
        with self.redis.pipeline() as pipe:
            for product_id in range(1, target_count + 1):
                pipe.zadd(self.products_key, {product_id: initial_timestamp})
            pipe.execute()


    def lock_least_updated_products_old(self, count: int) -> list[int]:
        # Retrieve the least recently updated products and lock them
        product_ids = self.redis.zrange(self.products_key, 0, count - 1)
        locked_products = []

        for product_id in product_ids:
            lock_key = f"{self.lock_key_prefix}{product_id}"
            # Attempt to acquire lock using SETNX
            if self.redis.setnx(lock_key, 1):  # Lock is acquired
                self.redis.expire(lock_key, 30)  # Set expiration for lock (optional)
                locked_products.append(int(product_id))

        return locked_products


    def lock_least_updated_products(self, count: int) -> list[int]:
        # Lua script to select and lock least updated products
        lua_script = """
        local locked_products = {}
        local total_locked = 0
        local products_key = KEYS[1]  -- Key for the sorted set of products
        local lock_key_prefix = ARGV[1]  -- Prefix for lock keys
        local desired_count = tonumber(ARGV[2])  -- Desired number of products to lock

        local products = redis.call('ZRANGE', products_key, 0, -1)  -- Get all products

        for _, product_id in ipairs(products) do
            -- Check if the product is already locked
            if redis.call('GET', lock_key_prefix .. product_id) == false then
                -- Lock the product by setting a lock key
                redis.call('SET', lock_key_prefix .. product_id, 'locked', 'EX', 120)  -- Expires in 2 minutes
                table.insert(locked_products, product_id)  -- Store the locked product ID
                total_locked = total_locked + 1

                -- Stop if we have locked the desired count of products
                if total_locked >= desired_count then
                    break
                end
            end
        end
        
        return locked_products
        """

        # Execute Lua script with the products key and the lock key prefix
        locked_product_ids = self.redis.eval(lua_script, 1, self.products_key, self.lock_key_prefix, count)

        return [int(product_id) for product_id in locked_product_ids]


    def update_unlock_products(self, product_ids: list[int]):
        '''Unlock products updating last access time'''
        current_time = int(time.time())  # Get current Unix timestamp in seconds
        
        with self.redis.pipeline() as pipe:
            for product_id in product_ids:
                # Update the timestamp for each product
                pipe.zadd(self.products_key, {product_id: current_time})
                # Remove the lock after updating
                pipe.delete(f"{self.lock_key_prefix}{product_id}")
            pipe.execute()


    def unlock_products(self, product_ids: list[int]):
        # Unlock the products without updating their last access time
        with self.redis.pipeline() as pipe:
            for product_id in product_ids:
                # Remove the lock for each product without updating timestamp
                pipe.delete(f"{self.lock_key_prefix}{product_id}")
            pipe.execute()
