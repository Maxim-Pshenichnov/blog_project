from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentCreateRequest(BaseModel):
    """DTO для создания комментария"""
    content: str = Field(..., max_length=500, example="Круто!")
    post_id: int = Field(..., example=1)
    author_id: int = Field(..., example=2)

class CommentUpdateRequest(BaseModel):
    """DTO для обновления комментария"""
    content: Optional[str] = Field(None, max_length=500)

class CommentResponse(BaseModel):
    """DTO для ответа с данными комментария"""
    id: int = Field(..., example=1)
    content: str = Field(..., example="Круто!")
    post_id: int = Field(..., example=1)
    author_id: int = Field(..., example=2)
    created_at: datetime = Field(..., example="2025-01-01T00:00:00")

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}