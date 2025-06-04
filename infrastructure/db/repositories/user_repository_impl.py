from sqlalchemy.orm import Session
from core.entities.user import User
from infrastructure.db.models.user_model import UserDB
from datetime import datetime

class UserRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        db_user = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_username(self, username: str) -> User | None:
        db_user = self.session.query(UserDB).filter(UserDB.username == username).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_email(self, email: str) -> User | None:
        db_user = self.session.query(UserDB).filter(UserDB.email == email).first()
        return self._to_domain(db_user) if db_user else None

    def save(self, user: User) -> User:
        if user.id:
            db_user = self.session.get(UserDB, user.id)
            if not db_user:
                raise ValueError("User not found")

            db_user.username = user.username
            db_user.email = user.email
            db_user.hashed_password = user.hashed_password
        else:
            db_user = self._to_db(user)
            self.session.add(db_user)
        
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_domain(db_user)

    def delete(self, user_id: int) -> bool:
        db_user = self.session.get(UserDB, user_id)
        if not db_user:
            return False
        
        self.session.delete(db_user)
        self.session.commit()
        return True

    def get_all(self) -> list[User]:
        return [self._to_domain(u) for u in self.session.query(UserDB).all()]

    def _to_domain(self, db_user: UserDB) -> User:
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at if hasattr(db_user, 'created_at') else datetime.now(),
            updated_at=datetime.now()
        )

    def _to_db(self, user: User) -> UserDB:
        return UserDB(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )