from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Comment(BaseModel):
    id: Optional[int] = None
    content: str
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }