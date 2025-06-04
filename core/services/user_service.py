from passlib.context import CryptContext
from typing import Optional
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from application.dto.user import UserCreateRequest, UserUpdateRequest
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repo: UserRepository, db_session: Session):
        self.user_repo = user_repo
        self.db_session = db_session

    def register_user(self, user_data: UserCreateRequest) -> User:
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")
        
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")

        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return self.user_repo.save(user)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id: int, user_data: UserUpdateRequest) -> User:
        existing_user = self.user_repo.get_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")

        if user_data.username and user_data.username != existing_user.username:
            if self.user_repo.get_by_username(user_data.username):
                raise ValueError("Username already taken")

        if user_data.email and user_data.email != existing_user.email:
            if self.user_repo.get_by_email(user_data.email):
                raise ValueError("Email already registered")

        updated_user = User(
            id=user_id,
            username=user_data.username or existing_user.username,
            email=user_data.email or existing_user.email,
            hashed_password=(
                pwd_context.hash(user_data.password) 
                if user_data.password 
                else existing_user.hashed_password
            )
        )
        
        return self.user_repo.save(updated_user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete(user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user