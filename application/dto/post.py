from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostCreateRequest(BaseModel):
    """DTO для создания поста"""
    title: str = Field(..., max_length=100, example="Мой первый пост")
    content: str = Field(..., example="Текст...")
    author_id: int = Field(..., example=1)

class PostUpdateRequest(BaseModel):
    """DTO для обновления поста"""
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = Field(None, min_length=10)

class PostResponse(BaseModel):
    """DTO для ответа с данными поста"""
    id: int = Field(..., example=1)
    title: str = Field(..., example="Мой первый пост")
    content: str = Field(..., example="Текст...")
    author_id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2025-01-01T00:00:00")

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}