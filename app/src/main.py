from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import psutil
import time

app = FastAPI(title="Container Health Dashboard")

templates = Jinja2Templates(directory="templates")

start_time = time.time()

@app.get("/health")
def healthcheck():
    return {"status": "ok"}
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
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