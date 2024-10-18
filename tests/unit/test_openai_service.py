import pytest
from fastapi import status
from fastapi.testclient import TestClient
from typing import Optional, Dict, Any

from ..services.openai_service import openai_service
from ..schemas.request_schema import RequestSchema
from ..utils.exceptions import APIError, NotFoundError, DatabaseError
from ..models.request import RequestModel
from ..database import engine, SessionLocal, Base
from unittest.mock import patch

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

# Test data for requests
REQUEST_DATA = {
    "prompt": "Write a short story about a dog and a cat.",
    "model": "text-davinci-003",
    "temperature": 0.7
}

# Test data for OpenAI API responses
MOCK_OPENAI_RESPONSE = {
    "choices": [
        {
            "text": "Once upon a time, there was a dog named Sparky..."
        }
    ]
}

# Mock data for cached responses
MOCK_CACHED_RESPONSE = "Once upon a time, there was a dog named Sparky..."

# Unit test cases for OpenAI service
class TestOpenAIService:
    # Test case for processing a valid request
    @pytest.mark.asyncio
    async def test_process_request_valid(self, db):
        with patch('openai.Completion.create', return_value=MOCK_OPENAI_RESPONSE):
            response = await openai_service.process_request(REQUEST_DATA)
            assert response == MOCK_OPENAI_RESPONSE["choices"][0]["text"].strip()

    # Test case for handling API errors during request processing
    @pytest.mark.asyncio
    async def test_process_request_api_error(self):
        with patch('openai.Completion.create', side_effect=openai.error.APIError):
            with pytest.raises(APIError):
                await openai_service.process_request(REQUEST_DATA)

    # Test case for handling unexpected errors during request processing
    @pytest.mark.asyncio
    async def test_process_request_unexpected_error(self):
        with patch('openai.Completion.create', side_effect=Exception):
            with pytest.raises(APIError):
                await openai_service.process_request(REQUEST_DATA)

    # Test case for fetching available OpenAI models
    @pytest.mark.asyncio
    async def test_get_available_models(self):
        with patch('openai.Model.list', return_value={"data": [{"id": "text-davinci-003"}]}):
            models = await openai_service.get_available_models()
            assert models == [{"id": "text-davinci-003"}]

    # Test case for handling API errors during model fetching
    @pytest.mark.asyncio
    async def test_get_available_models_api_error(self):
        with patch('openai.Model.list', side_effect=openai.error.APIError):
            with pytest.raises(APIError):
                await openai_service.get_available_models()

    # Test case for handling unexpected errors during model fetching
    @pytest.mark.asyncio
    async def test_get_available_models_unexpected_error(self):
        with patch('openai.Model.list', side_effect=Exception):
            with pytest.raises(APIError):
                await openai_service.get_available_models()

    # Test case for retrieving details for a specific OpenAI model
    @pytest.mark.asyncio
    async def test_get_model_details(self):
        with patch('openai.Model.retrieve', return_value={"data": {"id": "text-davinci-003"}}):
            model_details = await openai_service.get_model_details("text-davinci-003")
            assert model_details == {"id": "text-davinci-003"}

    # Test case for handling API errors during model detail retrieval
    @pytest.mark.asyncio
    async def test_get_model_details_api_error(self):
        with patch('openai.Model.retrieve', side_effect=openai.error.APIError):
            with pytest.raises(APIError):
                await openai_service.get_model_details("text-davinci-003")

    # Test case for handling model not found errors during model detail retrieval
    @pytest.mark.asyncio
    async def test_get_model_details_not_found(self):
        with patch('openai.Model.retrieve', side_effect=openai.error.APIError(code="not_found")):
            with pytest.raises(NotFoundError):
                await openai_service.get_model_details("text-davinci-003")

    # Test case for handling unexpected errors during model detail retrieval
    @pytest.mark.asyncio
    async def test_get_model_details_unexpected_error(self):
        with patch('openai.Model.retrieve', side_effect=Exception):
            with pytest.raises(APIError):
                await openai_service.get_model_details("text-davinci-003")

    # Test case for checking if cached response exists and returns it
    @pytest.mark.asyncio
    async def test_process_request_cached_response(self):
        with patch('openai.Completion.create', return_value=MOCK_OPENAI_RESPONSE):
            with patch('..utils.cache.cache_handler.get', return_value=MOCK_CACHED_RESPONSE):
                response = await openai_service.process_request(REQUEST_DATA)
                assert response == MOCK_CACHED_RESPONSE

    # Test case for caching response if not cached
    @pytest.mark.asyncio
    async def test_process_request_cache_response(self):
        with patch('openai.Completion.create', return_value=MOCK_OPENAI_RESPONSE):
            with patch('..utils.cache.cache_handler.get', return_value=None):
                with patch('..utils.cache.cache_handler.set') as mock_set:
                    response = await openai_service.process_request(REQUEST_DATA)
                    mock_set.assert_called_once_with(REQUEST_DATA, MOCK_OPENAI_RESPONSE["choices"][0]["text"].strip())

# Test cases for database service
class TestDBService:
    @pytest.mark.asyncio
    async def test_create_settings(self, db):
        settings = await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        assert settings.api_key == SETTINGS_DATA["api_key"]
        assert settings.preferred_model == SETTINGS_DATA["preferred_model"]

    @pytest.mark.asyncio
    async def test_get_settings(self, db):
        await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        settings = await db_service.get_settings(db, USER_ID)
        assert settings.api_key == SETTINGS_DATA["api_key"]

    @pytest.mark.asyncio
    async def test_update_settings(self, db):
        await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        updated_data = {"preferred_model": "text-curie-001"}
        updated_settings = await db_service.update_settings(db, SettingsSchema(**updated_data), USER_ID)
        assert updated_settings.preferred_model == updated_data["preferred_model"]

    @pytest.mark.asyncio
    async def test_delete_settings(self, db):
        await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        await db_service.delete_settings(db, USER_ID)
        settings = await db_service.get_settings(db, USER_ID)
        assert settings is None

    @pytest.mark.asyncio
    async def test_get_settings_not_found(self, db):
        with pytest.raises(NotFoundError):
            await db_service.get_settings(db, "nonexistent_user")

    @pytest.mark.asyncio
    async def test_update_settings_not_found(self, db):
        with pytest.raises(NotFoundError):
            await db_service.update_settings(db, SettingsSchema(**SETTINGS_DATA), "nonexistent_user")

    @pytest.mark.asyncio
    async def test_delete_settings_not_found(self, db):
        with pytest.raises(NotFoundError):
            await db_service.delete_settings(db, "nonexistent_user")

    @pytest.mark.asyncio
    async def test_create_settings_duplicate(self, db):
        await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        with pytest.raises(DatabaseError) as exc:
            await db_service.create_settings(db, SettingsSchema(**SETTINGS_DATA), USER_ID)
        assert "Failed to create settings." in str(exc.value)