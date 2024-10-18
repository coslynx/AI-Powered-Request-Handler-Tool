import os
from dotenv import load_dotenv
from typing import Dict, Any

class Settings:
    """
    Class to manage environment variables for the application.
    Loads variables from a .env file using python-dotenv.
    """

    def __init__(self):
        load_dotenv()

        # OpenAI API key
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not found.")

        # Database connection URL
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable not found.")

        # Default OpenAI model to use
        self.DEFAULT_OPENAI_MODEL: str = os.getenv("DEFAULT_OPENAI_MODEL", "text-davinci-003")

        # Logging level
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")

        # Cache settings
        self.CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", False)
        self.CACHE_EXPIRATION_TIME: int = int(os.getenv("CACHE_EXPIRATION_TIME", 3600))

        # Custom cache implementation
        self.CUSTOM_CACHE_IMPLEMENTATION: str = os.getenv("CUSTOM_CACHE_IMPLEMENTATION", None)

        # Error tracking service settings
        self.ERROR_TRACKING_SERVICE: str = os.getenv("ERROR_TRACKING_SERVICE", None)
        self.ERROR_TRACKING_API_KEY: str = os.getenv("ERROR_TRACKING_API_KEY", None)

        # Custom configuration variables
        self.CUSTOM_CONFIG_VARIABLE1: Any = os.getenv("CUSTOM_CONFIG_VARIABLE1", None)
        self.CUSTOM_CONFIG_VARIABLE2: Any = os.getenv("CUSTOM_CONFIG_VARIABLE2", None)


settings = Settings()