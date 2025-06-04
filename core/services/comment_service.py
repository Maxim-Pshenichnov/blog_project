from typing import Optional
from core.entities.comment import Comment
from core.repositories.post_repository import PostRepository
from core.repositories.user_repository import UserRepository
from core.repositories.comment_repository import CommentRepository
from application.dto.comment import CommentCreateRequest, CommentUpdateRequest
from sqlalchemy.orm import Session

class CommentService:
    def __init__(self, comment_repo: CommentRepository, 
                 post_repo: PostRepository,
                 user_repo: UserRepository,
                 db_session: Session):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.user_repo = user_repo
        self.db_session = db_session

    def create_comment(self, comment_data: CommentCreateRequest) -> Comment:
        if not self.post_repo.get_by_id(comment_data.post_id):
            raise ValueError("Post does not exist")
        
        if not self.user_repo.get_by_id(comment_data.author_id):
            raise ValueError("User does not exist")

        comment = Comment(
            content=comment_data.content,
            post_id=comment_data.post_id,
            author_id=comment_data.author_id
        )
        return self.comment_repo.save(comment)

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.comment_repo.get_by_id(comment_id)

    def get_all_comments(self) -> list[Comment]:
        return self.comment_repo.get_all()

    def update_comment(self, comment_id: int, comment_data: CommentUpdateRequest) -> Comment:
        comment = self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")

        updated_comment = Comment(
            id=comment_id,
            content=comment_data.content or comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id,
            created_at=comment.created_at
        )
        
        return self.comment_repo.save(updated_comment)

    def delete_comment(self, comment_id: int) -> bool:
        return self.comment_repo.delete(comment_id)

    def get_comments_by_post(self, post_id: int) -> list[Comment]:
        return self.comment_repo.get_by_post(post_id)