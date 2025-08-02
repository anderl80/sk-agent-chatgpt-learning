from fastapi import FastAPI, HTTPException
from app.kernel import create_kernel
from app.redis_memory import RedisMemory
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.contents.utils.author_role import AuthorRole


memory = RedisMemory()
app = FastAPI(title="Semantic Kernel Learning Lab")

# Initialize kernel once at startup
kernel = create_kernel()

@app.get("/chat")
async def chat(message: str):
    """Simple chat endpoint"""
    try:
        chat_service = list(kernel.services.values())[0]
        
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
    """Chat mit Semantic Kernel Redis Memory"""
    try:
        chat_service = list(kernel.services.values())[0]
        
        # Chat History aus Redis laden (mit integriertem Reducer)
        chat_history = await memory.get_chat_history(user, max_messages=20)
        
        # Neue User-Nachricht hinzufügen
        chat_history.add_user_message(message)
        
        settings = OpenAIChatPromptExecutionSettings(max_tokens=500, temperature=0.7)
        result = await chat_service.get_chat_message_contents(chat_history, settings)
        
        # Assistant Antwort zur History hinzufügen
        chat_history.add_assistant_message(result[0].content)
        
        # Komplette History speichern
        await memory.save_chat_history(user, chat_history)
        
        return {"response": result[0].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))