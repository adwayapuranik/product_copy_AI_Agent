import os
import json
import docx
import PyPDF2
import pandas as pd
from datetime import datetime

PROMPT_HISTORY_PATH = "data/instructions/prompt_history.json"
REQUIRED_COLUMNS = ["variantGroupCode", "productcopy"]
SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".docx"]


def ensure_dirs():
    os.makedirs("data/instructions", exist_ok=True)
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)

def read_file_content(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {SUPPORTED_EXTENSIONS}")

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".docx":
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif ext == ".pdf":
        content = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        return content

def is_json_file_empty(file_path: str) -> bool:
    absolute_path_checked = os.path.abspath(file_path)
    print(f"!!! DEBUG PATH CHECK: {absolute_path_checked}") 
    
    if not os.path.exists(file_path):
        # This is the line of code that is returning True (file not found)
        # Even though you see the file via 'ls -l'
        return True
    if not os.path.exists(file_path):
        return True
    if os.path.getsize(file_path) == 0:
        return True
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return not bool(data)
    except json.JSONDecodeError:
        return True

def add_prompt_entry(file_path: str, path: str, prompt_text: str):
    data = {}
    if os.path.exists(file_path) and not is_json_file_empty(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    date_entries = data.get(today, {})
    next_index = str(max(map(int, date_entries.keys()), default=0) + 1)
    date_entries[next_index] = [prompt_text, os.path.basename(path)]
    data[today] = date_entries

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Prompt added for {today} as entry #{next_index}")


def get_latest_prompt(file_path: str):
    if not os.path.exists(file_path) or is_json_file_empty(file_path):
        return None, None

    with open(file_path, "r") as f:
        data = json.load(f)

    latest_date = max(data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
    latest_idx = max(data[latest_date].keys(), key=lambda i: int(i))
    prompt_text, filename = data[latest_date][latest_idx]
    return prompt_text, filename


def validate_input_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    except Exception as e:
        raise FileNotFoundError(f"[ERROR] Failed to read file {file_path}: {e}")
    
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    print(f"[INFO] Initial rows: {len(df)}")
    df.drop_duplicates(subset=["variantGroupCode"], keep='first', inplace=True)    
    print(f"[INFO] Rows after deduplication (on 'variantGroupCode'): {len(df)}")
   
    return df


def invoke_bedrock(prompt: str, input_file: str):
    print("\n[Stub] Invoking AWS Bedrock model...")
    print(f"Prompt source: {input_file}")
    return pd.DataFrame(
        {"product_name": ["Sample"], "validated_copy": ["Example output"]}
    )


def get_bedrock_invoke_payload() -> dict:
    """getter method for bedrock payload"""

    payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": ""
                        }
                    ]
                }
            ],
        }
    
    return payload