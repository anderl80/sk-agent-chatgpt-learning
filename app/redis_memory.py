# app/redis_memory.py
import redis
import json
import os

class RedisMemory:
    def __init__(self, host="localhost", port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def get_history(self, user_id):
        key = f"chat:{user_id}:history"
        history = self.r.lrange(key, 0, -1)
        return [json.loads(msg) for msg in history]

    def add_message(self, user_id, role, content):
        key = f"chat:{user_id}:history"
        msg = json.dumps({"role": role, "content": content})
        self.r.rpush(key, msg)

    def clear_history(self, user_id):
        self.r.delete(f"chat:{user_id}:history")
