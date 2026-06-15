import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
DEEPAI_KEY = os.getenv("DEEPAI_API_KEY")

def colorize(image_path: str) -> str:
    """POSTs image to DeepAI colorizer endpoint and returns output URL"""
    if not DEEPAI_KEY or "your_deepai_key_here" in DEEPAI_KEY:
        raise HTTPException(status_code=400, detail="DeepAI API Key is missing or not set in your .env file.")
        
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://api.deepai.org/api/colorizer",
            files={"image": f},
            headers={"api-key": DEEPAI_KEY},
        )
    
    data = response.json()
    
    # Check if DeepAI actually returned the processed image link
    if "output_url" in data:
        return data["output_url"]
    else:
        # If DeepAI sent an error (like 'Quickstart key limit reached' or 'Invalid API key')
        error_msg = data.get("err", data.get("status", "Unknown API Error"))
        raise HTTPException(status_code=400, detail=f"DeepAI Service Error: {error_msg}")