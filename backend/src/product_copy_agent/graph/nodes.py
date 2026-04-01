import os
from datetime import datetime
from typing import Dict, Any

from product_copy_agent.aws.bedrock_invoke import BedrockInvokeModel
from product_copy_agent.utils import (
    ensure_dirs,
    is_json_file_empty,
    add_prompt_entry,
    get_latest_prompt,
    validate_input_file,
    PROMPT_HISTORY_PATH,
    read_file_content,
)

LEFT = "left"
VARIANT_GROUP_CODE = "variantGroupCode"


def check_prompt_history_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\nChecking existing prompt history...")
    ensure_dirs()
    state["prompt_exists"] = not is_json_file_empty(PROMPT_HISTORY_PATH)
    return state


def ask_user_update_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\nSkipping CLI prompt, expecting frontend to supply user_choice.")
    # print("\nWould you like to upload a new validation instruction file? (yes/no)")
    # choice = input("→ ").strip().lower()
    # state["user_choice"] = choice ##state["user_choice"] is already set via API
    # state["messages"].append(HumanMessage(content=f"User choice: {state.get('user_choice')}"))
    return state


def upload_instructions_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\nProcessing instruction file upload (via API).")
    path = state.get("instruction_file")
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Instruction file not found at {path}")

    new_instructions = read_file_content(path)

    # Bedrock invocation
    bedrock_obj = BedrockInvokeModel()
    updated_prompt = bedrock_obj._generate_new_dynamic_prompt(file_content=new_instructions)

    #updated_prompt = new_instructions  # stub

    add_prompt_entry(PROMPT_HISTORY_PATH, path, updated_prompt)
    print("Instructions uploaded and saved successfully.\n")

    latest_prompt, filename = get_latest_prompt(file_path=PROMPT_HISTORY_PATH)
    state["latest_prompt"] = latest_prompt
    state["logs"].append(f"Uploaded instructions from {os.path.basename(path)}")

    return state


def upload_input_file_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Processing input file upload (via API, not CLI).")
    path = state.get("input_file")
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found at {path}")

    df = validate_input_file(path)
    print("Input file validated successfully.\n")

    state["input_file_df"] = df
    # state["messages"].append(HumanMessage(content=f"Uploaded input file: {path}"))
    return state


def process_bedrock_node(state: Dict[str, Any]) -> Dict[str, Any]:
    import pandas as pd
    from datetime import datetime
    from src.product_copy_agent.utils import get_latest_prompt, PROMPT_HISTORY_PATH

    #prompt not in state
    if not state.get("latest_prompt"):
        prompt_text, prompt_filename = get_latest_prompt(file_path=PROMPT_HISTORY_PATH)
        state["latest_prompt"] = prompt_text
        state["prompt_filename_used"] = prompt_filename
    else:
        # if latest_prompt already in state
        _, prompt_filename = get_latest_prompt(file_path=PROMPT_HISTORY_PATH)
        state["prompt_filename_used"] = prompt_filename

    print(f"[DEBUG] Using prompt file: {state.get('prompt_filename_used')}")
    print(f"[DEBUG] Prompt content (first ~200 chars): {state['latest_prompt'][:200]}")

    # Bedrock invocation
    bedrock_obj = BedrockInvokeModel()
    print("Running validation with AWS Bedrock…")
    validated_product_copies = bedrock_obj.run_batch_invoke(state["latest_prompt"], state["input_file_df"])
    dfxa = state["input_file_df"]

    # print("Running validation in stub.")
    # validated_product_copies = [
    #     { VARIANT_GROUP_CODE: row.variantGroupCode,
    #       "validated_product_copy": row.productcopy }
    #     for row in dfxa.itertuples(index=False)
    # ]

    pc_df = pd.DataFrame(validated_product_copies)
    merged_df = dfxa.merge(pc_df, on=VARIANT_GROUP_CODE, how=LEFT)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/output/validated_product_copies_{timestamp}.xlsx"
    merged_df.to_excel(output_path, index=False)
    state["output_file"] = output_path
    state["prompt_preview_used"] = state["latest_prompt"][:200]

    return state


def generate_output_link_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"\nValidation completed. Output saved at: {state.get('output_file')}\n")
    return state
