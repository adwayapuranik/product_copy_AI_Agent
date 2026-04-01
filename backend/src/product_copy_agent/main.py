from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from product_copy_agent.api.routers import prompt_history, instructions, input_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt_history.router, prefix="/prompt-history", tags=["Prompt History"])
app.include_router(instructions.router, prefix="/instructions", tags=["Instructions"])
app.include_router(input_file.router, prefix="/input-file", tags=["Input File"])

@app.get("/")
def root():
    return {"message": "Product Copy Agent Backend is running."}
