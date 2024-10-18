import pytest
from fastapi import status
from fastapi.testclient import TestClient
from typing import Optional

from ..services.db_service import db_service
from ..schemas.settings_schema import SettingsSchema, SettingsResponseSchema
from ..utils.exceptions import APIError, NotFoundError, DatabaseError
from ..models.settings import SettingsModel
from ..database import engine, SessionLocal, Base

# Create a database session for testing
@pytest.fixture(scope="session")
def db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    # Create a database session
    db = SessionLocal()
    # Yield the session
    try:
        yield db
    finally:
        # Close the session and remove all tables after the test
        db.close()
        Base.metadata.drop_all(bind=engine)

# Mock user ID
USER_ID = "test_user"

# Test data for settings
SETTINGS_DATA = {
    "api_key": "sk-test-api-key",
    "preferred_model": "text-davinci-003",
    "is_cache_enabled": False,
    "cache_expiration_time": 3600,
}

# Create settings test cases
@pytest.mark.asyncio
async def test_create_settings(db):
    # Create settings using db_service.create_settings
    settings = await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    # Assert settings object is created with correct data
    assert settings.api_key == SETTINGS_DATA["api_key"]
    assert settings.preferred_model == SETTINGS_DATA["preferred_model"]
    assert settings.is_cache_enabled == SETTINGS_DATA["is_cache_enabled"]
    assert settings.cache_expiration_time == SETTINGS_DATA["cache_expiration_time"]

# Get settings test cases
@pytest.mark.asyncio
async def test_get_settings(db):
    # Create settings first for testing
    await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    # Get settings using db_service.get_settings
    settings = await db_service.get_settings(db, USER_ID)
    # Assert retrieved settings object matches the created data
    assert settings.api_key == SETTINGS_DATA["api_key"]
    assert settings.preferred_model == SETTINGS_DATA["preferred_model"]

# Update settings test cases
@pytest.mark.asyncio
async def test_update_settings(db):
    # Create settings first for testing
    await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    # Update settings data
    updated_data = {"preferred_model": "text-curie-001"}
    # Update settings using db_service.update_settings
    updated_settings = await db_service.update_settings(db, SettingsSchema(**updated_data), USER_ID)
    # Assert updated settings object has the new preferred model
    assert updated_settings.preferred_model == updated_data["preferred_model"]

# Delete settings test cases
@pytest.mark.asyncio
async def test_delete_settings(db):
    # Create settings first for testing
    await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    # Delete settings using db_service.delete_settings
    await db_service.delete_settings(db, USER_ID)
    # Assert settings are deleted by checking if they are not found
    settings = await db_service.get_settings(db, USER_ID)
    assert settings is None

# Error handling test cases
@pytest.mark.asyncio
async def test_get_settings_not_found(db):
    # Attempt to get settings for a non-existent user
    with pytest.raises(NotFoundError):
        await db_service.get_settings(db, "nonexistent_user")

@pytest.mark.asyncio
async def test_update_settings_not_found(db):
    # Attempt to update settings for a non-existent user
    with pytest.raises(NotFoundError):
        await db_service.update_settings(db, SettingsSchema(**SETTINGS_DATA), "nonexistent_user")

@pytest.mark.asyncio
async def test_delete_settings_not_found(db):
    # Attempt to delete settings for a non-existent user
    with pytest.raises(NotFoundError):
        await db_service.delete_settings(db, "nonexistent_user")

@pytest.mark.asyncio
async def test_create_settings_duplicate(db):
    # Create settings for the same user twice
    await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    with pytest.raises(DatabaseError) as exc:
        await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
    # Assert the database error message
    assert "Failed to create settings." in str(exc.value)