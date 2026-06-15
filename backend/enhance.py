from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services import colorize_image, upscale_image
import tempfile
import os

router = APIRouter()

@router.post("/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    mode: str = Form(default="auto")
):
    suffix = os.path.splitext(file.filename)[1]
    
    # Save incoming upload to a temporary file disk path
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        try:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            tmp.close() # Release file lock for processing
            
            # Replicating the routing logic based on user configuration selection
            # Auto mode defaults to performing a full double-enhancement chain for maximum impact
            if mode == "auto":
                execution_steps = ["colorize", "upscale"]
            else:
                execution_steps = [mode]
                
            final_url = None
            current_working_file = tmp_path
            temp_files_to_clean = []
            
            # Step A: Run Colorizer if needed
            if "colorize" in execution_steps:
                import requests
                color_url = colorize_image(current_working_file)
                
                # Download intermediate image to pipe into the upscale tool next
                img_data = requests.get(color_url).content
                tmp_color = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                tmp_color.write(img_data)
                tmp_color.close()
                
                current_working_file = tmp_color.name
                temp_files_to_clean.append(tmp_color.name)
                final_url = color_url
                
            # Step B: Run Upscaler if needed
            if "upscale" in execution_steps:
                final_url = upscale_image(current_working_file)
                
            # Clean up intermediate pipeline files
            for path in temp_files_to_clean:
                if os.path.exists(path):
                    os.unlink(path)
                    
            return JSONResponse({
                "success": True,
                "final_url": final_url,
                "pipeline_steps_executed": execution_steps
            })
            
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)}, status_code=500)
            
        finally:
            # Final disk file cleanup guard
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)