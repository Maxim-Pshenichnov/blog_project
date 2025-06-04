from typing import Optional
from core.entities.post import Post
from core.repositories.post_repository import PostRepository
from core.repositories.user_repository import UserRepository
from application.dto.post import PostCreateRequest, PostUpdateRequest
from sqlalchemy.orm import Session

class PostService:
    def __init__(self, post_repo: PostRepository, user_repo: UserRepository, db_session: Session):
        self.post_repo = post_repo
        self.user_repo = user_repo
        self.db_session = db_session

    def create_post(self, post_data: PostCreateRequest) -> Post:
        if not self.user_repo.get_by_id(post_data.author_id):
            raise ValueError("Author does not exist")
        
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=post_data.author_id
        )
        return self.post_repo.save(new_post)

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.post_repo.get_by_id(post_id)

    def get_all_posts(self) -> list[Post]:
        return self.post_repo.get_all()

    def update_post(self, post_id: int, post_data: PostUpdateRequest) -> Post:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")

        update_data = post_data.model_dump(exclude_unset=True)
        updated_post = Post(
            id=post_id,
            title=update_data.get('title', post.title),
            content=update_data.get('content', post.content),
            author_id=post.author_id,
            created_at=post.created_at
        )
        
        return self.post_repo.save(updated_post)

    def delete_post(self, post_id: int) -> bool:
        return self.post_repo.delete(post_id)

    def get_posts_by_author(self, author_id: int) -> list[Post]:
        return self.post_repo.get_by_author(author_id)