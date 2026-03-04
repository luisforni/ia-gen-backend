import ollama
import json
import os
from pathlib import Path
from app.core.config import settings

class OllamaService:
    @staticmethod
    def _load_system_prompt():
        prompts_path = Path(__file__).parent.parent / "config" / "prompts.json"
        
        try:
            if prompts_path.exists():
                with open(prompts_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('system_prompt', '')
            return ''
        except Exception:
            return ''

    @staticmethod
    async def chat_stream(messages):
        system_prompt = OllamaService._load_system_prompt()
        
        messages_with_system = messages
        if system_prompt and (not messages or messages[0].get('role') != 'system'):
            messages_with_system = [
                {'role': 'system', 'content': system_prompt}
            ] + messages
        
        client = ollama.AsyncClient(host=settings.OLLAMA_HOST)
        
        response = await client.chat(
            model=settings.MODEL_NAME,
            messages=messages_with_system,
            stream=True
        )
        
        async for chunk in response:
            content = chunk.get('message', {}).get('content', '')
            
            if content:
                yield content