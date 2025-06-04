from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }