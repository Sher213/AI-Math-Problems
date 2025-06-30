from fastapi import FastAPI, WebSocket, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from typing import List
import json
import asyncio
from datetime import datetime
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import pytesseract

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Store active connections
active_connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the received data (text from camera)
            response = await process_study_help(data)
            await websocket.send_text(json.dumps({
                "type": "response",
                "content": response,
                "timestamp": datetime.now().isoformat()
            }))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)

async def process_study_help(text: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant. Provide clear, concise explanations."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing request: {str(e)}"

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Process the image and extract text
    # This is a placeholder - you'll need to implement actual image processing
    return {"message": "Image processed successfully"}

class OcrRequest(BaseModel):
    image: str

@app.post("/ocr")
async def ocr_endpoint(request: OcrRequest):
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        image = Image.open(BytesIO(image_data))
        # Perform OCR
        text = pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)