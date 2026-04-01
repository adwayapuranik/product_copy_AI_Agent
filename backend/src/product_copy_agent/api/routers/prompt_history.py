from fastapi import APIRouter
from product_copy_agent.utils import is_json_file_empty, PROMPT_HISTORY_PATH

router = APIRouter()

@router.get("/exists")
def check_prompt_history_exists():
    exists = not is_json_file_empty(PROMPT_HISTORY_PATH)
    return {"exists": exists}
