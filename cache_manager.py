import os
import json
import redis  # INSTALLATION: pip install redis

# ==========================================
# ⚡ REDIS CACHE CONFIGURATION
# ==========================================
# Settings for high-performance caching
# ==========================================
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB_INDEX = int(os.getenv("REDIS_DB", "0"))
DEFAULT_TTL = int(os.getenv("CACHE_TTL", "300")) # 5 minutes

class CacheManager:
    """
    Wrapper for Redis operations to store temporary data.
    """
    
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=REDIS_HOST, 
                port=REDIS_PORT, 
                db=REDIS_DB_INDEX
            )
            self.client.ping() # Check connection
            print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        except redis.ConnectionError:
            print("Warning: Redis is unreachable.")

    def set_value(self, key: str, value: dict):
        """Serializes and saves a dictionary to cache."""
        self.client.setex(key, DEFAULT_TTL, json.dumps(value))

    def get_value(self, key: str):
        """Retrieves and deserializes data."""
        data = self.client.get(key)
        return json.loads(data) if data else None

    def flush_all(self):
        """DANGER: Clears the cache database."""
        # Safety check could go here
        self.client.flushdb()

if __name__ == "__main__":
    cache = CacheManager()
    cache.set_value("user_session", {"id": 123, "role": "admin"})
    print(cache.get_value("user_session"))
