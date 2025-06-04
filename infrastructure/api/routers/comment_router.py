from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from application.dto.comment import (
    CommentCreateRequest,
    CommentUpdateRequest,
    CommentResponse
)
from core.services.comment_service import CommentService
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post(
    "/", 
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_comment(
    comment_data: CommentCreateRequest,
    service: CommentService = Depends(Provide[Container.comment_service])
):
    """Создание нового комментария"""
    try:
        return service.create_comment(comment_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[CommentResponse])
@inject
async def get_all_comments(
    service: CommentService = Depends(Provide[Container.comment_service])
):
    """Получение всех комментариев"""
    return service.get_all_comments()

@router.get("/{comment_id}", response_model=CommentResponse)
@inject
async def get_comment(
    comment_id: int,
    service: CommentService = Depends(Provide[Container.comment_service])
):
    """Получение комментария по ID"""
    comment = service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comment

@router.put("/{comment_id}", response_model=CommentResponse)
@inject
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdateRequest,
    service: CommentService = Depends(Provide[Container.comment_service])
):
    """Обновление комментария"""
    try:
        return service.update_comment(comment_id, comment_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_comment(
    comment_id: int,
    service: CommentService = Depends(Provide[Container.comment_service])
):
    """Удаление комментария"""
    if not service.delete_comment(comment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )