import asyncio
import os
import ollama

async def test_ollama():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    client = ollama.AsyncClient(host=host)
    messages = [{"role": "user", "content": "Hola, ¿cómo estás?"}]
    try:
        async for chunk in await client.chat(model="llama3.2:1b", messages=messages, stream=True):
            print(chunk)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())