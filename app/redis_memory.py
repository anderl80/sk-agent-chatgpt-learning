# app/redis_memory.py
import redis
import json
import os
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents import ChatHistoryTruncationReducer

class RedisMemory:
    def __init__(self, host="localhost", port=6379):
        # Modern Redis client for ChatHistory persistence
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    async def get_chat_history(self, user_id: str, max_messages: int = 20) -> ChatHistory:
        """Get chat history using Semantic Kernel ChatHistory APIs with SK Reducer"""
        key = f"chat:{user_id}:history"
        
        # Get serialized ChatHistory from Redis
        serialized_history = self.r.get(key)
        
        if not serialized_history:
            return ChatHistory()
        
        try:
            full_history = ChatHistory.restore_chat_history(serialized_history)
            
            # Use Semantic Kernel ChatHistoryTruncationReducer
            reducer = ChatHistoryTruncationReducer(
                messages=full_history.messages,
                target_count=max_messages,
                threshold_count=max_messages + 1,  # Reduce when exceeding max_messages
                auto_reduce=False  # Manual control
            )
            
            # Apply SK reducer
            await reducer.reduce()
            
            # Create new ChatHistory with reduced messages
            reduced_history = ChatHistory()
            for message in reducer.messages:
                reduced_history.add_message(message)
            
            return reduced_history
            
        except Exception as e:
            print(f"Error restoring chat history: {e}")
            return ChatHistory()

    async def save_chat_history(self, user_id: str, chat_history: ChatHistory):
        """Save chat history using Semantic Kernel ChatHistory APIs"""
        key = f"chat:{user_id}:history"
        
        try:
            serialized_history = chat_history.serialize()
            self.r.set(key, serialized_history)
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def get_history(self, user_id):
        """Legacy method - keep for compatibility"""
        key = f"chat:{user_id}:history"
        history = self.r.lrange(key, 0, -1)
        return [json.loads(msg) for msg in history]

    def add_message(self, user_id, role, content):
        """Legacy method - keep for compatibility"""
        key = f"chat:{user_id}:history"
        msg = json.dumps({"role": role, "content": content})
        self.r.rpush(key, msg)

    def clear_history(self, user_id):
        """Clear chat history"""
        self.r.delete(f"chat:{user_id}:history")
