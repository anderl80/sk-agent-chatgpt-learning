#!/usr/bin/env python3
"""
Simple CLI Chat Application for Semantic Kernel Learning Lab
"""
import requests
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

class ChatClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.username = None
    
    def check_health(self):
        """Check if the FastAPI server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def send_message(self, message: str, use_memory: bool = True):
        """Send message to the chat endpoint"""
        try:
            if use_memory and self.username:
                # Use /chat2 endpoint with memory
                params = {"user": self.username, "message": message}
                response = requests.get(f"{self.base_url}/chat2", params=params, timeout=30)
            else:
                # Use simple /chat endpoint
                params = {"message": message}
                response = requests.get(f"{self.base_url}/chat", params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"

def main():
    console.print(Panel.fit(
        "[bold blue]🤖 Semantic Kernel Chat CLI[/bold blue]\n"
        "[dim]Type 'quit' or 'exit' to leave[/dim]",
        border_style="blue"
    ))
    
    client = ChatClient()
    
    # Check server health
    if not client.check_health():
        console.print("❌ [red]Cannot connect to FastAPI server at http://localhost:8080[/red]")
        console.print("[dim]Make sure the server is running with: uvicorn app.main:app --reload[/dim]")
        sys.exit(1)
    
    console.print("✅ [green]Connected to server[/green]")
    
    # Ask for username for memory feature
    use_memory = Prompt.ask(
        "Do you want to use memory (chat history)?", 
        choices=["y", "n"], 
        default="y"
    ) == "y"
    
    if use_memory:
        client.username = Prompt.ask("Enter your username", default="user")
        console.print(f"[green]Using memory for user: {client.username}[/green]")
    else:
        console.print("[yellow]Using simple chat without memory[/yellow]")
    
    console.print("\n" + "="*50)
    console.print("[bold]Start chatting![/bold]")
    console.print("="*50 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            
            if not user_input.strip():
                continue
            
            # Show thinking indicator
            with console.status("[bold green]AI is thinking...", spinner="dots"):
                response = client.send_message(user_input, use_memory)
            
            # Display AI response with markdown formatting
            console.print("\n[bold green]🤖 AI Assistant:[/bold green]")
            
            # Try to render as markdown, fallback to plain text if it fails
            try:
                markdown = Markdown(response)
                console.print(Panel(markdown, border_style="green", padding=(0, 1)))
            except Exception:
                console.print(Panel(response, border_style="green", padding=(0, 1)))
            
            console.print()  # Empty line for spacing
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()