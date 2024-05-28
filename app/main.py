import logging
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infrastructure.docs.openapi_tags import openapi_tags
from .infrastructure.routers.auth_router import auth_router
from .infrastructure.routers.driver_router import driver_router
from .infrastructure.routers.driver_assignment_router import driver_assignment_router
from .infrastructure.routers.invitation_codes_router import invitation_code_router
from .infrastructure.routers.management_router import management_router
from .infrastructure.routers.vehicle_router import vehicle_router

load_dotenv()

app = FastAPI(
    title="Vehicle Management API",
    summary="API for managing vehicles and drivers of a transportation company",
    version="1.0.0",
    contact={
        "name": "Spaghetti scripters team",
        "email": "spaghetti-scripters@gmail.com"
    },
    openapi_tags=openapi_tags,
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

with open("log_conf.yaml", "rt") as f:
    config = yaml.safe_load(f.read())

# Configure the logging module with the config file
logging.config.dictConfig(config)
