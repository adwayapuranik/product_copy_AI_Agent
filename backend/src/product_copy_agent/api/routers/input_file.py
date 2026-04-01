import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from product_copy_agent.utils import (
    ensure_dirs,
    validate_input_file,
    get_latest_prompt,
    PROMPT_HISTORY_PATH,
)
from product_copy_agent.graph.state import initial_state
from product_copy_agent.graph.graph_builder import build_graph

router = APIRouter()
ensure_dirs()

@router.post("/upload")
async def upload_input_file(file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in [".xlsx", ".xls", ".csv"]:
        raise HTTPException(status_code=400, detail="Unsupported input file type")

    tmp_name = f"data/input/tmp_input_{uuid.uuid4().hex}{ext}"
    with open(tmp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file.file.close()

    try:
        df = validate_input_file(tmp_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Input file validation failed: {e}")

    latest_prompt, _ = get_latest_prompt(PROMPT_HISTORY_PATH)
    if not latest_prompt:
        raise HTTPException(status_code=400, detail="No instruction prompt available. Please upload instructions first.")

    state = initial_state()
    state["latest_prompt"] = latest_prompt
    state["input_file"] = tmp_name
    state["input_file_df"] = df

    app_graph = build_graph()
    final_state = app_graph.invoke(state)

    output_path = final_state.get("output_file")
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Failed to generate output file.")

    return FileResponse(path=output_path, filename=os.path.basename(output_path),
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
