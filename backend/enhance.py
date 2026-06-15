from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile
import os
from agent import run_ai_orchestration

router = APIRouter()

@router.post("/enhance")
async def enhance_image(
    file: UploadFile = File(...),
    mode: str = Form(default="auto")
):
    suffix = os.path.splitext(file.filename)[1]

    # save incoming upload to file disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        try: 
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            tmp.close() # close access block so other functions can open it

            # RUn our chained service pipeline
            agent_result = run_ai_orchestration(tmp_path, mode)
            return JSONResponse(agent_result)
        
        except Exception as e: 
            return JSONResponse({"success": False, "error": str(e)}, status_code=500)
        
        finally:
            if os.path.exsists(tmp_path):
                os.unlink(tmp_path)