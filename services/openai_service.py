from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from .utils.logger import logger
from .utils.exceptions import APIError, NotFoundError
from .utils.cache import cache_handler
from .config import settings
import openai
import json

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def process_request(self, request_data: Dict[str, Any]) -> str:
        """
        Processes a user request using the OpenAI API.

        Args:
            request_data (Dict[str, Any]): Data containing the prompt, model selection, and parameters.

        Returns:
            str: The response text from OpenAI.

        Raises:
            APIError: If an error occurs during the OpenAI API call.
        """
        try:
            # Check if the response is cached
            cached_response = await cache_handler.get(request_data)
            if cached_response:
                logger.info("Using cached response.")
                return cached_response

            # Send the request to the OpenAI API
            response = openai.Completion.create(
                engine=request_data.get("model", settings.DEFAULT_OPENAI_MODEL),
                prompt=request_data["prompt"],
                temperature=request_data.get("temperature", 0.7),
                max_tokens=request_data.get("max_tokens"),
                top_p=request_data.get("top_p"),
                frequency_penalty=request_data.get("frequency_penalty"),
                presence_penalty=request_data.get("presence_penalty"),
            )

            # Extract the response text
            response_text = response.choices[0].text.strip()

            # Cache the response
            await cache_handler.set(request_data, response_text)

            # Return the response text
            return response_text

        except openai.error.APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise APIError(detail=f"OpenAI API Error: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise APIError(detail=f"Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_available_models(self) -> Optional[Dict[str, Any]]:
        """
        Fetches available OpenAI models.

        Returns:
            Optional[Dict[str, Any]]: A dictionary of available models.
        """
        try:
            models = openai.Model.list()
            return models.data
        except openai.error.APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise APIError(detail=f"OpenAI API Error: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise APIError(detail=f"Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_model_details(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves details for a specific OpenAI model.

        Args:
            model_id (str): The ID of the OpenAI model.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing model details.
        """
        try:
            model_details = openai.Model.retrieve(model_id)
            return model_details.data
        except openai.error.APIError as e:
            if e.code == "not_found":
                logger.warning(f"OpenAI Model not found: {model_id}")
                raise NotFoundError(detail=f"OpenAI Model not found: {model_id}")
            else:
                logger.error(f"OpenAI API Error: {e}")
                raise APIError(detail=f"OpenAI API Error: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise APIError(detail=f"Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

openai_service = OpenAIService()