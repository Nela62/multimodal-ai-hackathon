from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables (including SAMBANOVA_API_KEY from .env)
load_dotenv()

from llama_index.llms.sambanovasystems import SambaNovaCloud
from llama_index.core.base.llms.types import ChatMessage, MessageRole

# Instantiate the SambaNovaCloud model with the chosen model
llm = SambaNovaCloud(
    model="DeepSeek-R1-Distill-Llama-70B",
    context_window=100000,
    max_tokens=1024,
    temperature=0.7,
    top_k=1,
    top_p=0.01,
)

app = FastAPI()

# Define request and response models
class ChatRequest(BaseModel):
    # Expect a list of messages; each message should be a dict with "role" and "content"
    messages: list[dict]

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # Convert the incoming messages to ChatMessage objects
    messages = []
    for msg in req.messages:
        role_str = msg.get("role", "user").lower()
        if role_str == "system":
            role = MessageRole.SYSTEM
        elif role_str == "assistant":
            role = MessageRole.ASSISTANT
        else:
            role = MessageRole.USER
        messages.append(ChatMessage(role=role, content=msg.get("content", "")))
    
    # Use the SambaNova model to get a chat response
    ai_msg = llm.chat(messages)
    return ChatResponse(answer=ai_msg.message.content)

# Optional: if you wish to run the endpoint directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
