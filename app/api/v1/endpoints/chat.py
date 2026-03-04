import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.services.ollama_service import OllamaService
from app.core.rate_limiter import limiter
import uuid

router = APIRouter()

@router.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    formatted_messages = [m.model_dump() for m in chat_request.messages]
    
    async def event_generator():
        full_response = ""
        
        async for chunk in OllamaService.chat_stream(formatted_messages):
            full_response += chunk
            event = {
                "type": "text_delta",
                "text": chunk
            }
            yield f'data: {json.dumps(event)}\n\n'
        
        message_id = str(uuid.uuid4())
        final_event = {
            "type": "message_delta",
            "delta": {
                "role": "assistant",
                "content": full_response
            },
            "id": message_id
        }
        yield f'data: {json.dumps(final_event)}\n\n'

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )