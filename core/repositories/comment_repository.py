from abc import ABC, abstractmethod
from core.entities.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    def get_by_id(self, comment_id: int) -> Comment:
        pass

    @abstractmethod
    def save(self, comment: Comment) -> None:
        pass

    @abstractmethod
    def delete(self, comment_id: int) -> None:
        pass