from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.dto.post import (
    PostCreateRequest,
    PostUpdateRequest,
    PostResponse
)
from core.services.post_service import PostService
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "/", 
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_post(
    post_data: PostCreateRequest,
    service: PostService = Depends(Provide[Container.post_service])
):
    """Создание нового поста"""
    try:
        return service.create_post(post_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[PostResponse])
@inject
async def get_all_posts(
    service: PostService = Depends(Provide[Container.post_service])
):
    """Получение всех постов"""
    return service.get_all_posts()

@router.get("/{post_id}", response_model=PostResponse)
@inject
async def get_post(
    post_id: int,
    service: PostService = Depends(Provide[Container.post_service])
):
    """Получение поста по ID"""
    post = service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.put("/{post_id}", response_model=PostResponse)
@inject
async def update_post(
    post_id: int,
    post_data: PostUpdateRequest,
    service: PostService = Depends(Provide[Container.post_service])
):
    """Обновление поста"""
    try:
        return service.update_post(post_id, post_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_post(
    post_id: int,
    service: PostService = Depends(Provide[Container.post_service])
):
    """Удаление поста"""
    if not service.delete_post(post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )