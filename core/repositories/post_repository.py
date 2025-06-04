from abc import ABC, abstractmethod
from core.entities.post import Post

class PostRepository(ABC):
    @abstractmethod
    def get_by_id(self, post_id: int) -> Post:
        pass

    @abstractmethod
    def save(self, post: Post) -> None:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> None:
        pass