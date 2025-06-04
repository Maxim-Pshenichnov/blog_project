from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.dto.user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse
)
from core.services.user_service import UserService
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_user(
    user_data: UserCreateRequest,
    service: UserService = Depends(Provide[Container.user_service])
):
    """Создание нового пользователя"""
    try:
        return service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[UserResponse])
@inject
async def get_all_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    """Получение списка всех пользователей"""
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
@inject
async def get_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service])
):
    """Получение пользователя по ID"""
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    service: UserService = Depends(Provide[Container.user_service])
):
    """Обновление данных пользователя"""
    try:
        return service.update_user(user_id, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service])
):
    """Удаление пользователя"""
    if not service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )