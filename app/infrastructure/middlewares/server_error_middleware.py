from typing import Union
from fastapi import Response
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

class ServerErrorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request, call_next) -> Union[JSONResponse, Response]:
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"API RESPONSE 500 - {request.method} {request.url} - {str(e)}")
            return JSONResponse(status_code=500, content={"error": str(e)})