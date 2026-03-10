import os
import json
import socket
import uuid
import time
import sys
import logging
from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# Configure standard logging to use stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["endpoint"])
pod_name = os.getenv("HOSTNAME", socket.gethostname())

@app.get("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return {"status": "ok"}

@app.get("/hello")
def hello(request: Request):
    REQUEST_COUNT.labels(endpoint="/hello").inc() 
    
    trace_id = str(uuid.uuid4())
    current_time = time.time()
    status_code = 200
    
    log_payload = {
        "severity": "INFO",
        "timestamp": current_time,
        "trace_id": trace_id,
        "pod": pod_name,
        "status": status_code,
        "endpoint": "/hello",
        "message": f"Request processed by {pod_name}",
        "app": "hello-service" # Added this to match Loki filters
    }
    
    # Using print(json.dumps) is the most reliable way in Python 3.x 
    # for containerd to capture the line immediately.
    print(json.dumps(log_payload), flush=True)
    
    return {
        "status": status_code,
        "timestamp": current_time,
        "pod": pod_name,
        "trace_id": trace_id,
        "message": "Hello from the platform-cluster!"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)