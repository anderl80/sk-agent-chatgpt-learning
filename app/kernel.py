import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

load_dotenv()

def create_kernel():
    """Create a minimal Semantic Kernel instance"""
    kernel = Kernel()
    
    # Azure OpenAI setup
    chat_service = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
    kernel.add_service(chat_service)
    
    return kernel
