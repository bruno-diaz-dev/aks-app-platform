from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from prometheus_client import Counter, generate_latest


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR.parent / "templates"

import psutil
import time

app = FastAPI(title="Container Health Dashboard")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

start_time = time.time()

@app.get("/health")
def healthcheck():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return {"status": "ok"}
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    REQUEST_COUNT.labels(endpoint="/").inc()
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_info = psutil.virtual_memory()
    memory_usage_mb = round(memory_info.used / (1024 * 1024), 2)

    uptime_seconds = int(time.time() - start_time)
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cpu": cpu_usage,
            "memory": memory_usage_mb,
            "uptime": uptime,
        }
    )

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )