"""
Routes for user management.

Includes endpoints for creating, retrieving, and updating user information.
"""

from fastapi import APIRouter, Depends, Form, HTTPException, Query, responses, status
from sqlalchemy.orm import Session

from foundever.core import database
from foundever.domains.commons import schemas as commons_schemas
from foundever.domains.users import exceptions, processes, schemas
from foundever.interfaces.users import schemas as users_schemas

router = APIRouter()


@router.post(
    "/v1/users/",
    response_model=users_schemas.UserResponse,
    tags=["Users"],
    responses={
        400: {
            "description": "Bad Request",
            "model": commons_schemas.ErrorResponse,
        }
    },
)
async def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(database.get_db),
) -> responses.JSONResponse:
    try:
        user = processes.create_user(db=db, user_data=user_data)
    except exceptions.UsernameAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code_transaction": "UNABLE_TO_CREATE_USER",
                "message": str(e),
            },
        ) from e

    return responses.JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code_transaction": "OK",
            "user_id": user.id,
        },
    )


@router.put(
    "/v1/users/",
    response_model=users_schemas.UserResponse,
    tags=["Users"],
    responses={
        400: {
            "description": "Bad Request",
            "model": commons_schemas.ErrorResponse,
        }
    },
)
async def update_user(
    user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
) -> responses.JSONResponse:
    try:
        user = processes.update_user(db=db, user_data=user_data)
    except exceptions.UserDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code_transaction": "UNABLE_TO_UPDATE_USER",
                "message": str(e),
            },
        ) from e

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code_transaction": "OK",
            "user_id": user.id,
        },
    )


@router.delete(
    "/v1/users/",
    response_model=users_schemas.DeleteResponse,
    tags=["Users"],
    responses={
        400: {
            "description": "Bad Request",
            "model": commons_schemas.ErrorResponse,
        }
    },
)
async def delete_user(
    username: str = Form(
        ...,
    ),
    db: Session = Depends(database.get_db),
) -> responses.JSONResponse:
    try:
        processes.delete_user(db=db, username=username)
    except exceptions.UserDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code_transaction": "UNABLE_TO_DELETE_USER",
                "message": str(e),
            },
        ) from e

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code_transaction": "OK",
            "message": "OK",
        },
    )


@router.get(
    "/v1/users/",
    response_model=users_schemas.UserRetrieveResponse,
    tags=["Users"],
    responses={
        400: {
            "description": "Bad Request",
            "model": commons_schemas.ErrorResponse,
        }
    },
)
async def get_users(
    username: str | None = Query(
        default=None,
        description="Optional filter to retrieve user by their username.",
    ),
    db: Session = Depends(database.get_db),
) -> responses.JSONResponse:
    users_data = processes.retrieve_users(db=db, username=username)
    data = [user.model_dump() for user in users_data]

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code_transaction": "OK",
            "data": data,
        },
    )
