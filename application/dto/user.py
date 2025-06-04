from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateRequest(BaseModel):
    """DTO для создания пользователя"""
    username: str = Field(..., min_length=3, max_length=50, example="ivan_ivanov")
    email: EmailStr = Field(..., example="ivan@example.com")
    password: str = Field(..., min_length=8, example="qwerty123")

class UserUpdateRequest(BaseModel):
    """DTO для обновления пользователя"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, example="new_username")
    email: Optional[EmailStr] = Field(None, example="new_email@example.com")
    password: Optional[str] = Field(None, min_length=8, example="newpassword123")

class UserResponse(BaseModel):
    """DTO для ответа с данными пользователя"""
    id: int = Field(..., example=1)
    username: str = Field(..., example="ivan_ivanov")
    email: EmailStr = Field(..., example="ivan@example.com")

    class Config:
        from_attributes = True