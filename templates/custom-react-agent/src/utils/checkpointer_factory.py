from langgraph.checkpoint.memory import MemorySaver
from src.utils.redis_checkpointer import AsyncRedisSaver
from src.config import settings
from src.utils.logger import logger


class CheckpointerFactory:
    _redis_pool = None

    @classmethod
    async def create_checkpointer(cls, checkpointer_type: str, **kwargs):
        """Create a checkpointer based on the type and kwargs."""
        logger.info(f"Creating checkpointer of type: {checkpointer_type}")
        if checkpointer_type == "in_memory":
            return MemorySaver()
        elif checkpointer_type == "redis":
            max_connections = kwargs.get("max_connections", 10)

            # Async redis saver already handles connection pooling
            async with AsyncRedisSaver.from_url(
                url=settings.REDIS_URL, max_connections=max_connections
            ) as redis_saver:
                return redis_saver
        else:
            raise ValueError(f"Invalid checkpointer type: {checkpointer_type}")
