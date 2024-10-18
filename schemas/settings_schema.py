from pydantic import BaseModel, validator, Field

class SettingsSchema(BaseModel):
    """
    Schema for validating user settings data.

    Attributes:
        api_key (str): User's API key for OpenAI.
        preferred_model (str): User's preferred OpenAI model (e.g., "text-davinci-003").
        is_cache_enabled (bool): Flag indicating whether caching is enabled for requests.
        cache_expiration_time (int): Time in seconds for cache expiration.

    Raises:
        ValueError: If the API key is invalid.
    """

    api_key: str = Field(..., description="User's API key for OpenAI.")
    preferred_model: str = Field("text-davinci-003", description="User's preferred OpenAI model.")
    is_cache_enabled: bool = Field(False, description="Flag indicating whether caching is enabled.")
    cache_expiration_time: int = Field(3600, description="Time in seconds for cache expiration.")

    @validator("api_key")
    def api_key_validation(cls, value):
        """
        Validates the API key format.

        Args:
            value (str): The API key to validate.

        Returns:
            str: The validated API key.

        Raises:
            ValueError: If the API key is invalid.
        """
        if not value:
            raise ValueError("API key cannot be empty.")
        # Add specific API key validation logic here (e.g., length, characters, pattern)
        return value