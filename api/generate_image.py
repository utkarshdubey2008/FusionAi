from fastapi import FastAPI, HTTPException
import aiohttp
import uuid
import re

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Generation API"}

@app.get("/generate")
async def generate_image(prompt: str):
    payload = {
        "messages": [{"content": prompt, "role": "user"}],
        "user_id": str(uuid.uuid4()),
        "codeModelMode": True,
        "agentMode": {
            "mode": True,
            "id": "ImageGenerationLV45LJp",
            "name": "Image Generation"
        },
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36"
    }

    api_url = "https://www.blackbox.ai/api/chat"

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as response:
            if response.status == 200:
                response_text = await response.text()
                link = re.search(r"(https://storage\.googleapis\.com/[^\)]+)", response_text)
                if link:
                    return {"image_url": link.group()}
                else:
                    raise HTTPException(status_code=404, detail="No image found")
            else:
                raise HTTPException(status_code=response.status, detail="Error from image generation service")
