import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from product_copy_agent.utils import (
    ensure_dirs,
    read_file_content,
    add_prompt_entry,
    get_latest_prompt,
    PROMPT_HISTORY_PATH,
)
from product_copy_agent.aws.bedrock_invoke import BedrockInvokeModel

router = APIRouter()
ensure_dirs()

@router.post("/upload")
async def upload_instructions(file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in [".txt", ".docx", ".pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported instruction file type")

    tmp_name = f"data/instructions/tmp_{uuid.uuid4().hex}{ext}"
    with open(tmp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file.file.close()

    content = read_file_content(tmp_name)

    bedrock = BedrockInvokeModel()
    updated_prompt = bedrock._generate_new_dynamic_prompt(file_content=content)
    #updated_prompt = content  # stub

    add_prompt_entry(PROMPT_HISTORY_PATH, tmp_name, updated_prompt)
    prompt_text, filename = get_latest_prompt(PROMPT_HISTORY_PATH)

    # if not prompt_text:
    #     raise HTTPException(status_code=500, detail="Failed to update prompt history")    
    #return {"status": "success", "code": 200, "message": "Instruction file uploaded and prompt updated successfully."}

    return {"filename": filename, "prompt_text": prompt_text}
