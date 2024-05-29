from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.configs.initial_data import add_default_user
from app.infrastructure.configs.sql_database import create_db_and_tables

from .infrastructure.docs.openapi_tags import openapi_tags
from .infrastructure.routers.auth_router import auth_router
from .infrastructure.routers.driver_router import driver_router
from .infrastructure.routers.driver_assignment_router import driver_assignment_router
from .infrastructure.routers.invitation_codes_router import invitation_code_router
from .infrastructure.routers.management_router import management_router
from .infrastructure.routers.vehicle_router import vehicle_router


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    create_db_and_tables()
    add_default_user()
    yield
    print("Application shutdown")

app = FastAPI(
    title="Vehicle Management API",
    summary="API for managing vehicles and drivers of a transportation company",
    version="1.0.0",
    contact={
        "name": "Spaghetti scripters team",
        "email": "spaghetti-scripters@gmail.com"
    },
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["Authorization"])
app.include_router(driver_router, prefix="/driver", tags=["Driver"])
app.include_router(
    driver_assignment_router, prefix="/driver-assignment", tags=["Driver assignment"]
)
app.include_router(
    invitation_code_router, prefix="/invitation-code", tags=["Invitation code"]
)
app.include_router(management_router, prefix="/management", tags=["Management"])
app.include_router(vehicle_router, prefix="/vehicles", tags=["Vehicle"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.add_middleware("http")
async def log_server_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code >= 500:
            logger.error(f"API RESPONSE {response.status_code} - {request.method} {request.url} - {response.body.decode('utf-8')}")
        return response
    except Exception as e:
        logger.error(f"API RESPONSE 500 - {request.method} {request.url} - {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

logger.remove(0)
logger.add(
    "logs/app.log",
    format="{time} | {level} | {message}",
    level="DEBUG",
)
