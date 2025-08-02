from fastapi import FastAPI, HTTPException
from app.kernel import create_kernel

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
