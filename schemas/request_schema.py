from pydantic import BaseModel, validator, Field
from typing import Optional

class RequestSchema(BaseModel):
    """
    Schema for validating user request data for processing text using OpenAI.

    Attributes:
        prompt (str): The text prompt to be processed by OpenAI.
        model (str): The OpenAI model to use for processing (e.g., "text-davinci-003").
        temperature (float):  A value between 0 and 1 that controls the randomness of the output.
        max_tokens (Optional[int]): The maximum number of tokens to generate in the response.
        top_p (Optional[float]):  A value between 0 and 1 that controls the diversity of the output.
        frequency_penalty (Optional[float]):  A value between -2.0 and 2.0 that penalizes the model for generating text that it has already generated.
        presence_penalty (Optional[float]):  A value between -2.0 and 2.0 that penalizes the model for generating text that is similar to the input text.

    Raises:
        ValueError: If the prompt is empty or the model is invalid.
    """

    prompt: str = Field(..., description="The text prompt to be processed by OpenAI.")
    model: str = Field("text-davinci-003", description="The OpenAI model to use for processing.")
    temperature: float = Field(0.7, description="A value between 0 and 1 that controls the randomness of the output.")
    max_tokens: Optional[int] = Field(None, description="The maximum number of tokens to generate in the response.")
    top_p: Optional[float] = Field(None, description="A value between 0 and 1 that controls the diversity of the output.")
    frequency_penalty: Optional[float] = Field(None, description="A value between -2.0 and 2.0 that penalizes the model for generating text that it has already generated.")
    presence_penalty: Optional[float] = Field(None, description="A value between -2.0 and 2.0 that penalizes the model for generating text that is similar to the input text.")

    @validator("prompt")
    def prompt_validation(cls, value):
        """
        Validates the prompt field.

        Args:
            value (str): The prompt to validate.

        Returns:
            str: The validated prompt.

        Raises:
            ValueError: If the prompt is empty.
        """
        if not value:
            raise ValueError("Prompt cannot be empty.")
        return value

    @validator("model")
    def model_validation(cls, value):
        """
        Validates the OpenAI model field.

        Args:
            value (str): The model to validate.

        Returns:
            str: The validated model.

        Raises:
            ValueError: If the model is invalid.
        """
        # Add validation logic to ensure the model is a valid OpenAI model. 
        # For example, check against a list of supported models or use a regular expression.
        return value

class RequestResponseSchema(BaseModel):
    """
    Schema for formatting the response from OpenAI.
    """
    status: str
    response: str