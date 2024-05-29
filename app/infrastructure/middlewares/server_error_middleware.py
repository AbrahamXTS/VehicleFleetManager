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
            response = await call_next(request)
            if response.status_code >= 500:
                logger.error(f"API RESPONSE {response.status_code} - {request.method} {request.url} - {response.body.decode('utf-8')}")
            return response
        except Exception as e:
            logger.error(f"API RESPONSE 500 - {request.method} {request.url} - {str(e)}")
            return JSONResponse(status_code=500, content={"error": str(e)})