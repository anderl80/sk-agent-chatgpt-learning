# Semantic Kernel Learning Lab

A minimal example for learning Semantic Kernel with Azure OpenAI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your Azure OpenAI credentials:
```
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Use

- **Chat**: `GET /chat?message=Hello`
- **Health**: `GET /health`

Example:
```bash
curl "http://localhost:8080/chat?message=Hello"
```
