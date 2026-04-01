import multiprocessing
import uvicorn

num_cores = multiprocessing.cpu_count()
workers = max(1, num_cores)  # at least 1 worker

print(f"Starting uvicorn with {workers} worker(s)")

uvicorn.run(
    "product_copy_agent.main:app",
    host="0.0.0.0",
    port=8000,
    workers=workers,
)
