import os
import json
import socket
import uuid
import time
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total", ["endpoint", "status"])
pod_name = os.getenv("HOSTNAME", socket.gethostname())

# --- 1. Custom Exception Handler for 404/Generic Errors ---
# This ensures that even for "Not Found", you get a trace_id in the response body.
@app.exception_handler(Exception)
@app.exception_handler(404)
async def custom_error_handler(request: Request, exc):
    status_code = getattr(exc, "status_code", 500)
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "status_code": status_code,
            "trace_id": trace_id,
            "message": str(exc.detail) if hasattr(exc, "detail") else "Internal Server Error",
            "path": request.url.path
        }
    )

# --- 2. Middleware for Correlation and Logging ---
class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Generate trace_id at the start
        request.state.trace_id = str(uuid.uuid4())
        
        # Process request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        status_code = response.status_code
        
        # Unified Log Payload
        log_payload = {
            "severity": "INFO" if status_code < 400 else "ERROR",
            "timestamp": time.time(),
            "pod": pod_name,
            "endpoint": request.url.path,
            "status_code": status_code,
            "status": "ok" if status_code < 400 else "error",
            "duration": f"{process_time:.4f}s",
            "trace_id": request.state.trace_id,
            "app": "hello-service"
        }
        
        print(json.dumps(log_payload), flush=True)
        REQUEST_COUNT.labels(endpoint=request.url.path, status=status_code).inc()
        
        # Inject trace_id into headers
        response.headers["X-Trace-ID"] = request.state.trace_id
        return response

app.add_middleware(ObservabilityMiddleware)

# --- 3. Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok", "status_code": 200}

@app.get("/hello")
def hello(request: Request):
    return {
        "status": "ok",
        "status_code": 200,
        "timestamp": time.time(),
        "pod_name": pod_name,
        "trace_id": request.state.trace_id,
        "message": "Hello from the platform-cluster!"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
