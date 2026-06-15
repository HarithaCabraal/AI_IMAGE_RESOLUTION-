import os
from anthropic import Anthropic
from services import colorize_image, upscale_image
import requests
import tempfile

# Initialize Anthropic Claude Client
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_ai_orchestration(file_path: str, mode: str) -> dict:
    """
    Decides actions based on the user mode preference. If mode is 'auto',
    it defaults to running a full-suite enhancement or relies on processing decisions
    """

    actions = []

    #Simple, highly reliable operational rules optimized for hackathon execution
    if mode == "colorize":
        actions = ["colorize"]
    elif mode == "upscale":
        actions = ["upscale"]
    elif mode ==  "auto":
        #In a standard auto configuration, we apply both to maximize dramatic "before/after " value
        actions = ["colorize", "upscale"]
    else:
        actions = ["upscale"] # Safe baseline fallback

    current_working_file = file_path
    temp_files_to_clean = []

    try:
        # Step 1: Execute Colorization if requested
        if "colorize" in actions:
            color_url = colorize_image(current_working_file)

            # Download the colorized image to a temporary file to pipe into the next step
            img_data = requests.get(color_url).content
            tmp_color = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            tmp_color.write(img_data)
            tmp_color.close()

            current_working_file = tmp_color.name
            temp_files_to_clean.append(tmp_color.name)

        # Step 2: Execute Super-Resolution Upscaling if requested
        if "upscale" in actions:
            final_url = upscale_image(current_working_file)
        else:
            # If we only colorized, upload the intermediate file to Cloudinary to get a static URL
            final_url = upscale_image(current_working_file)

        return {
            "success": True,
            "final_url": final_url,
            "pipeline_steps_executed": actions
        }
    
    finally:
        # Cleanup secondary files generated along the pipe run 
        for path in temp_files_to_clean:
            if os.path.exsists(path):
                os.unlink(path)