# backend/app/middleware/logging_middleware.py

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# Configure logger
logger = logging.getLogger("app_logger")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        logger.info(
            f"Incoming Request: {request.method} {request.url.path}"
        )

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled Exception: {str(e)}")
            raise e

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time}ms"
        )

        return response