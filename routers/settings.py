from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

from ..models import SettingsModel
from ..schemas import SettingsSchema, SettingsResponseSchema
from ..services.db_service import db_service
from ..utils.exceptions import APIError
from ..utils.logger import logger

settings_router = APIRouter()

@settings_router.get("/", response_model=SettingsResponseSchema)
async def get_settings(current_user: str = None):
    try:
        settings = await db_service.get_settings(current_user)
        if not settings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
        return settings
    except Exception as e:
        logger.error(f"Error fetching settings: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch settings")

@settings_router.put("/", response_model=SettingsResponseSchema)
async def update_settings(settings_data: SettingsSchema, current_user: str = None):
    try:
        updated_settings = await db_service.update_settings(settings_data, current_user)
        if not updated_settings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
        return updated_settings
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update settings")

@settings_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_settings(current_user: str = None):
    try:
        await db_service.delete_settings(current_user)
    except Exception as e:
        logger.error(f"Error deleting settings: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete settings")