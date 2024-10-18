from sqlalchemy.orm import Session
from .models import SettingsModel, RequestModel
from .utils.logger import logger
from .utils.exceptions import APIError, NotFoundError, DatabaseError

# SQLAlchemy dependency injection
def get_db():
    # This function creates a database session (scoped)
    # It is a dependency injected into routes and services
    # It's the central point for accessing the database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Functions for managing user settings
async def create_settings(db: Session, settings_data: SettingsSchema, user_id: str):
    """Creates new user settings.

    Args:
        db (Session): Database session.
        settings_data (SettingsSchema): Data to create settings.
        user_id (str): User ID for the settings.

    Returns:
        SettingsModel: Created settings object.

    Raises:
        DatabaseError: If database error occurs.
    """
    try:
        new_settings = SettingsModel(**settings_data.dict(), user_id=user_id)
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings
    except Exception as e:
        logger.error(f"Error creating settings: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to create settings.")

async def get_settings(db: Session, user_id: str):
    """Retrieves settings for a user.

    Args:
        db (Session): Database session.
        user_id (str): User ID to retrieve settings.

    Returns:
        SettingsModel: Retrieved settings object.

    Raises:
        NotFoundError: If settings not found.
        DatabaseError: If database error occurs.
    """
    try:
        settings = db.query(SettingsModel).filter(SettingsModel.user_id == user_id).first()
        if not settings:
            raise NotFoundError(detail="Settings not found.")
        return settings
    except NotFoundError as e:
        logger.warning(f"Settings not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching settings: {e}")
        raise DatabaseError(detail="Failed to fetch settings.")

async def update_settings(db: Session, settings_data: SettingsSchema, user_id: str):
    """Updates settings for a user.

    Args:
        db (Session): Database session.
        settings_data (SettingsSchema): Data to update settings.
        user_id (str): User ID to update settings.

    Returns:
        SettingsModel: Updated settings object.

    Raises:
        NotFoundError: If settings not found.
        DatabaseError: If database error occurs.
    """
    try:
        settings = db.query(SettingsModel).filter(SettingsModel.user_id == user_id).first()
        if not settings:
            raise NotFoundError(detail="Settings not found.")
        for key, value in settings_data.dict(exclude_unset=True).items():
            setattr(settings, key, value)
        db.commit()
        db.refresh(settings)
        return settings
    except NotFoundError as e:
        logger.warning(f"Settings not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to update settings.")

async def delete_settings(db: Session, user_id: str):
    """Deletes settings for a user.

    Args:
        db (Session): Database session.
        user_id (str): User ID to delete settings.

    Raises:
        NotFoundError: If settings not found.
        DatabaseError: If database error occurs.
    """
    try:
        settings = db.query(SettingsModel).filter(SettingsModel.user_id == user_id).first()
        if not settings:
            raise NotFoundError(detail="Settings not found.")
        db.delete(settings)
        db.commit()
    except NotFoundError as e:
        logger.warning(f"Settings not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error deleting settings: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to delete settings.")

# Functions for managing user requests
async def create_request(db: Session, request_data: RequestSchema, user_id: str):
    """Creates a new user request.

    Args:
        db (Session): Database session.
        request_data (RequestSchema): Data for the request.
        user_id (str): User ID for the request.

    Returns:
        RequestModel: Created request object.

    Raises:
        DatabaseError: If database error occurs.
    """
    try:
        new_request = RequestModel(**request_data.dict(), user_id=user_id)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except Exception as e:
        logger.error(f"Error creating request: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to create request.")

async def get_request(db: Session, request_id: str):
    """Retrieves a request by ID.

    Args:
        db (Session): Database session.
        request_id (str): ID of the request.

    Returns:
        RequestModel: Retrieved request object.

    Raises:
        NotFoundError: If request not found.
        DatabaseError: If database error occurs.
    """
    try:
        request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
        if not request:
            raise NotFoundError(detail="Request not found.")
        return request
    except NotFoundError as e:
        logger.warning(f"Request not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching request: {e}")
        raise DatabaseError(detail="Failed to fetch request.")

async def update_request(db: Session, request_data: RequestSchema, request_id: str):
    """Updates a request by ID.

    Args:
        db (Session): Database session.
        request_data (RequestSchema): Data to update the request.
        request_id (str): ID of the request.

    Returns:
        RequestModel: Updated request object.

    Raises:
        NotFoundError: If request not found.
        DatabaseError: If database error occurs.
    """
    try:
        request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
        if not request:
            raise NotFoundError(detail="Request not found.")
        for key, value in request_data.dict(exclude_unset=True).items():
            setattr(request, key, value)
        db.commit()
        db.refresh(request)
        return request
    except NotFoundError as e:
        logger.warning(f"Request not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error updating request: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to update request.")

async def delete_request(db: Session, request_id: str):
    """Deletes a request by ID.

    Args:
        db (Session): Database session.
        request_id (str): ID of the request.

    Raises:
        NotFoundError: If request not found.
        DatabaseError: If database error occurs.
    """
    try:
        request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
        if not request:
            raise NotFoundError(detail="Request not found.")
        db.delete(request)
        db.commit()
    except NotFoundError as e:
        logger.warning(f"Request not found: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error deleting request: {e}")
        db.rollback()
        raise DatabaseError(detail="Failed to delete request.")