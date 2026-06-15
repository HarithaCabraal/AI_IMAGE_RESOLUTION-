import os
import requests
import cloudinary
import cloudinary.uploader
from fastapi import HTTPException

#Initialize Cloudinary Configuration from your .env secrets
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def colorize_image(file_path: str) -> str:
    """Sends a local image file path to the DeepAI Colorizer API and returns the processed image URL."""
    api_key = os.getenv("DEEPAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, details="Missing DEEPAI_API_KEY in environment variables.")
    
    try:
        with open(file_path, "rb") as image_file:
            response = requests.post(
                "https://api.deepai.org/api/colorizer",
                files={"image": image_file},
                headers={"api-key": api_key},
                timeout=30
            )

        response_data = response.json()
        if "output_url" in response_data:
            return response_data["output_url"]
        else:
            raise HTTPException(status_code=500, detail=f"DeepAI Error: {response_data.get('err', 'Unknown error')}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Colorization API: {str(e)}")
    

def upscale_image(file_path: str) -> str:
    """Uploads an image to Cloudinary and triggers their AI E_upscale effect overlay transformation. """
    try: 
        # Upload the file to your Cloudinary storage
        upload_result = cloudinary.uploader.upload(file_path)
        public_id = upload_result.get("public_id")
        format_extension = upload_result.get("format")

        if not public_id:
            raise HTTPException(status_code=500, details="Cloudinary upload failed to yeild a public_id.")
        
        # Build the transformation URL applying the Super-Resolution AI effect overlay
        upscaled_url = cloudinary.utils.cloudinary_url(
            f"{public_id}.{format_extension}",
            effect="upscale"
        )[0]

        return upscaled_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary processing exception: {str(e)}")
        
    