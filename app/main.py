from fastapi import FastAPI, HTTPException
from app.kernel import create_kernel
from app.redis_memory import RedisMemory


memory = RedisMemory()
app = FastAPI(title="Semantic Kernel Learning Lab")

# Initialize kernel once at startup
kernel = create_kernel()

@app.get("/chat")
async def chat(message: str):
    """Simple chat endpoint"""
    try:
        chat_service = list(kernel.services.values())[0]
        
        from semantic_kernel.contents.chat_history import ChatHistory
        from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
        
        chat_history = ChatHistory()
        chat_history.add_user_message(message)
        
        settings = OpenAIChatPromptExecutionSettings(max_tokens=500, temperature=0.7)
        result = await chat_service.get_chat_message_contents(chat_history, settings)
        
        return {"response": result[0].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/chat2")
async def chat2(user: str, message: str):
    """Chat mit Redis-Memory"""
    chat_service = list(kernel.services.values())[0]
    
    from semantic_kernel.contents.chat_history import ChatHistory
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings

    chat_history = ChatHistory()

    # Vorherige Nachrichten laden
    for msg in memory.get_history(user):
        if msg["role"] == "user":
            chat_history.add_user_message(msg["content"])
        else:
            chat_history.add_assistant_message(msg["content"])

    # Neue User-Nachricht einfügen
    chat_history.add_user_message(message)

    settings = OpenAIChatPromptExecutionSettings(max_tokens=500, temperature=0.7)
    result = await chat_service.get_chat_message_contents(chat_history, settings)

    # Antwort speichern
    memory.add_message(user, "user", message)
    memory.add_message(user, "assistant", result[0].content)

    return {"response": result[0].content}