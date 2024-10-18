from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("settings.id"), nullable=False)
    prompt = Column(String, nullable=False)
    model = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    response = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(String, nullable=False)  # Use appropriate datetime type

    user = relationship("SettingsModel", back_populates="requests")