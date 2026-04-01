# Product Copy Agent
AI Agent that validates Raw Product Copy against Instruction Set and produces perfectly compliant Validated Product Copy in an easily downloadable excel format.

# Prerequisites
* Backend
    1. Python 3.10+
    2. `uv` installed
    3. AWS credentials configured (for Bedrock access)

* Frontend
    1. Node.js 18+
    2. npm 9+

# Running the Application
You need two terminals:

# Terminal 1: Backend
   From the project root
   `uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000`

# Terminal 2: Frontend
     cd Frontend/my-project
     npm install
     npm run dev




