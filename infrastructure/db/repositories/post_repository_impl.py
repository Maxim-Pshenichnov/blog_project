from sqlalchemy.orm import Session
from core.entities.post import Post
from infrastructure.db.models.post_model import PostDB

class PostRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, post_id: int) -> Post | None:
        db_post = self.session.query(PostDB).filter(PostDB.id == post_id).first()
        return self._to_domain(db_post) if db_post else None

    def save(self, post: Post) -> Post:
        if post.id:
            db_post = self.session.get(PostDB, post.id)
            if not db_post:
                raise ValueError("Post not found")
            
            db_post.title = post.title
            db_post.content = post.content
            db_post.author_id = post.author_id
        else:
            db_post = self._to_db(post)
            self.session.add(db_post)
        
        self.session.commit()
        self.session.refresh(db_post)
        return self._to_domain(db_post)

    def delete(self, post_id: int) -> bool:
        db_post = self.session.query(PostDB).get(post_id)
        if not db_post:
            return False
        self.session.delete(db_post)
        self.session.commit()
        return True

    def get_all(self) -> list[Post]:
        return [self._to_domain(p) for p in self.session.query(PostDB).all()]

    def get_by_author(self, author_id: int) -> list[Post]:
        return [self._to_domain(p) for p in 
                self.session.query(PostDB).filter(PostDB.author_id == author_id).all()]

    def _to_domain(self, db_post: PostDB) -> Post:
        return Post(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            author_id=db_post.author_id,
            created_at=db_post.created_at
        )

    def _to_db(self, post: Post) -> PostDB:
        return PostDB(
            title=post.title,
            content=post.content,
            author_id=post.author_id,
            created_at=post.created_at
        )