from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from .database import Base

class SettingsModel(Base):
    __tablename__ = "settings"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    api_key = Column(String, nullable=False)
    preferred_model = Column(String, default="text-davinci-003")
    is_cache_enabled = Column(Boolean, default=False)
    cache_expiration_time = Column(Integer, default=3600)