from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

from .models import RequestModel
from .schemas import RequestSchema, RequestResponseSchema
from .services.openai_service import openai_service
from .utils.exceptions import APIError
from .utils.logger import logger

requests_router = APIRouter()

@requests_router.post("/", response_model=RequestResponseSchema)
async def process_request(request_data: RequestSchema):
    """
    Handles user requests to process text using OpenAI.

    Args:
        request_data (RequestSchema): Data containing the prompt, model selection, and parameters.

    Returns:
        JSONResponse: A JSON response containing the status and processed text from OpenAI.

    Raises:
        HTTPException: If the request data is invalid or an error occurs during processing.
    """
    try:
        # Validate request data using the RequestSchema
        validated_data = request_data.dict()
        
        # Process the request using the openai_service
        response = await openai_service.process_request(validated_data)
        
        # Format the response using the RequestResponseSchema
        formatted_response = RequestResponseSchema(
            status="success",
            response=response
        )
        
        # Return the formatted response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(formatted_response.dict())
        )
    except APIError as e:
        # Log the error
        logger.error(f"API Error: {e.detail}")
        
        # Return an error response with details
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder({"detail": e.detail})
        )
    except Exception as e:
        # Log the unexpected error
        logger.error(f"Unexpected Error: {e}")
        
        # Return a generic error response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail": "Internal Server Error"})
        )