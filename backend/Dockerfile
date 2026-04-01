# 1️⃣ Base image with Python
FROM python:3.12-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy dependency files first
COPY pyproject.toml README.md uv.lock ./

# 4️⃣  COPY source code BEFORE installation 
# The installer needs the source files present to properly set up the editable link.
COPY src/ ./src

# 5️⃣  Install uv and dependencies
RUN pip install uv
RUN uv pip install -e . --system --no-cache-dir

# 6️⃣ Set environment variables (optional: good practice)
ENV PYTHONUNBUFFERED=1

# 7️⃣ Expose API port
EXPOSE 8000

# 8️⃣ Run uvicorn via entrypoint script
ENV WORKERS=$(nproc)
CMD uvicorn product_copy_agent.main:app --host 0.0.0.0 --port 8000 
