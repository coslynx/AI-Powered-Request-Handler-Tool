from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from .config import settings
from .database import engine, Base
from .routers import requests_router, settings_router
from .utils.exceptions import APIError
from .utils.logger import logger
from .utils.cache import cache_handler
from .services.openai_service import openai_service
from .services.db_service import db_service

app = FastAPI(
    title="AI Powered Request Handler",
    version="1.0.0",
    description="A simple API for interacting with OpenAI's API"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database models
Base.metadata.create_all(bind=engine)

# Include routers for API endpoints
app.include_router(requests_router, prefix="/requests", tags=["Requests"])
app.include_router(settings_router, prefix="/settings", tags=["Settings"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    await cache_handler.init()
    logger.info("Cache initialized.")
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    await cache_handler.close()
    logger.info("Cache closed.")

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.error(f"API Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail})
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors()})
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)