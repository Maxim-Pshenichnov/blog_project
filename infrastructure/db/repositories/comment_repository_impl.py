from sqlalchemy.orm import Session
from core.entities.comment import Comment
from infrastructure.db.models.comment_model import CommentDB

class CommentRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, comment_id: int) -> Comment | None:
        db_comment = self.session.query(CommentDB).filter(CommentDB.id == comment_id).first()
        return self._to_domain(db_comment) if db_comment else None

    def save(self, comment: Comment) -> Comment:
        if comment.id:
            db_comment = self.session.get(CommentDB, comment.id)
            if not db_comment:
                raise ValueError("Comment not found")
            
            db_comment.content = comment.content
            db_comment.post_id = comment.post_id
            db_comment.author_id = comment.author_id
        else:
            db_comment = self._to_db(comment)
            self.session.add(db_comment)
        
        self.session.commit()
        self.session.refresh(db_comment)
        return self._to_domain(db_comment)

    def delete(self, comment_id: int) -> bool:
        db_comment = self.session.query(CommentDB).get(comment_id)
        if not db_comment:
            return False
        self.session.delete(db_comment)
        self.session.commit()
        return True

    def get_all(self) -> list[Comment]:
        return [self._to_domain(c) for c in self.session.query(CommentDB).all()]

    def get_by_post(self, post_id: int) -> list[Comment]:
        return [self._to_domain(c) for c in 
                self.session.query(CommentDB).filter(CommentDB.post_id == post_id).all()]

    def _to_domain(self, db_comment: CommentDB) -> Comment:
        return Comment(
            id=db_comment.id,
            content=db_comment.content,
            post_id=db_comment.post_id,
            author_id=db_comment.author_id,
            created_at=db_comment.created_at
        )

    def _to_db(self, comment: Comment) -> CommentDB:
        return CommentDB(
            content=comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id,
            created_at=comment.created_at
        )