"""
Logging Middleware
"""
import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate process time
        process_time = time.time() - start_time
        
        # Log the request
        logger.info(
            f"{request.method} {request.url.path} - Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )
        
        # Add custom header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
