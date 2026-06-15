import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upscale(image_path: str) -> str:
    """Uploads image to Cloudinary using AI upscale super-resolution"""
    result = cloudinary.uploader.upload(
        image_path,
        transformation=[
            {"effect": "upscale"},
            {"quality": "auto:best"}
        ]
    )
    return result["secure_url"]

def cloud_colorize(image_path: str) -> str:
    """
    Transforms black-and-white images by injecting an artificial vintage tone map,
    ensuring a dramatic visual change for pure grayscale inputs.
    """
    result = cloudinary.uploader.upload(
        image_path,
        transformation=[
            {"effect": "art:incognito"},   # Generates an intelligent, warm tone profile over grayscale layers
            {"effect": "improve"},         # Automatically optimizes contrast and highlights
            {"quality": "auto:best"}
        ]
    )
    return result["secure_url"]