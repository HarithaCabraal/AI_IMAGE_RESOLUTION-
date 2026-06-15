from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from cloudinary_service import upscale, cloud_colorize
import tempfile
import os

router = APIRouter()

@router.post("/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    mode: str = Form(default="auto")
):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        try:
            tmp.write(await file.read())
            tmp_path = tmp.name
            tmp.close() 
            
            if mode == "auto":
                selected_modes = ["colorize", "upscale"]
            else:
                selected_modes = [mode]
                
            result = {}
            current_working_file = tmp_path
            final_processed_url = ""
            
            # Step 1: Execute Free Color Enhancement via Cloudinary
            if "colorize" in selected_modes:
                color_url = cloud_colorize(current_working_file)
                result["colorized_url"] = color_url
                final_processed_url = color_url
                current_working_file = color_url  # Pass URL downstream if chaining auto mode
                
            # Step 2: Execute Super-Resolution Upscale via Cloudinary
            if "upscale" in selected_modes:
                # Cloudinary can accept a file path or a URL from a previous upload directly
                upscale_url = upscale(current_working_file)
                result["upscaled_url"] = upscale_url
                final_processed_url = upscale_url
                
            result["final_url"] = final_processed_url
            result["mode"] = mode
            result["success"] = True
            return JSONResponse(result)
            
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)}, status_code=500)
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)