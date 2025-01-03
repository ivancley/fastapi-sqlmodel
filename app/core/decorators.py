import functools
from fastapi import HTTPException, status
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DatabaseError,
    DataError,
    ProgrammingError,
    InvalidRequestError,
    InterfaceError,
    TimeoutError,
    SQLAlchemyError,
)


def handle_sqlalchemy_errors_async(func):
    @functools.wraps(func)
    async def wrapper(self, session, *args, **kwargs):
        try:
            return await func(self, session, *args, **kwargs)
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Erro de integridade: {str(e.orig)}",
            )
        except OperationalError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Operational error: {str(e)}"
            )
        except DatabaseError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except DataError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Data error: {str(e)}"
            )
        except ProgrammingError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Programming error: {str(e)}"
            )
        except InvalidRequestError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request error: {str(e)}"
            )
        except InterfaceError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Interface error: {str(e)}"
            )
        except TimeoutError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Timeout error: {str(e)}"
            )
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"SQLAlchemy error: {str(e)}"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )

    return wrapper
