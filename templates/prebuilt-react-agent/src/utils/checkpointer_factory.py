from langgraph.checkpoint.memory import MemorySaver
from src.utils.redis_checkpointer import AsyncRedisSaver
from redis.asyncio import ConnectionPool
from src.config import settings


class CheckpointerFactory:
    _redis_pool = None

    @classmethod
    async def create_checkpointer(cls, checkpointer_type: str, **kwargs):
        if checkpointer_type == "in_memory":
            return MemorySaver()
        elif checkpointer_type == "redis":
            # Get Redis connection parameters from kwargs or use defaults
            host = kwargs.get("redis_host", "localhost")
            port = kwargs.get("redis_port", 6379)
            db = kwargs.get("redis_db", 0)
            max_connections = kwargs.get("redis_max_connections", 10)

            # Use connection pooling for better performance
            async with AsyncRedisSaver.from_conn_info(
                host=host, port=port, db=db, max_connections=max_connections
            ) as redis_saver:
                return redis_saver
        else:
            raise ValueError(f"Invalid checkpointer type: {checkpointer_type}")

    @classmethod
    async def create_redis_checkpointer_with_shared_pool(cls, **kwargs):
        """Create a Redis checkpointer with a shared connection pool."""
        # Initialize the shared pool if it doesn't exist
        if cls._redis_pool is None:
            host = kwargs.get("redis_host", "localhost")
            port = kwargs.get("redis_port", 6379)
            db = kwargs.get("redis_db", 0)
            max_connections = kwargs.get("redis_max_connections", 50)

            cls._redis_pool = ConnectionPool(
                host=host, port=port, db=db, max_connections=max_connections
            )

        # Create a saver using the shared pool
        async with AsyncRedisSaver.from_pool(cls._redis_pool) as redis_saver:
            return redis_saver
