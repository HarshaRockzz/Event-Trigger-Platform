import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_set(key: str, value: dict, expiry: int = 3600):
    redis_client.setex(key, expiry, json.dumps(value))

def cache_get(key: str):
    value = redis_client.get(key)
    return json.loads(value) if value else None