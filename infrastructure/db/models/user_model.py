from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    posts = relationship("PostDB", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("CommentDB", back_populates="author", cascade="all, delete-orphan")