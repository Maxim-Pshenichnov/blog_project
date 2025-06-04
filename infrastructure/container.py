from dependency_injector import containers, providers
from infrastructure.db.database import SessionLocal

from infrastructure.db.repositories.comment_repository_impl import CommentRepositoryImpl
from infrastructure.db.repositories.post_repository_impl import PostRepositoryImpl
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl

from core.services.comment_service import CommentService
from core.services.post_service import PostService
from core.services.user_service import UserService

class Container(containers.DeclarativeContainer):

    db_session = providers.Singleton(SessionLocal)

    user_repository = providers.Factory(
        UserRepositoryImpl,
        session=db_session
    )
    
    post_repository = providers.Factory(
        PostRepositoryImpl,
        session=db_session
    )
    
    comment_repository = providers.Factory(
        CommentRepositoryImpl,
        session=db_session
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        db_session=db_session
    )
    
    post_service = providers.Factory(
        PostService,
        post_repo=post_repository,
        user_repo=user_repository,
        db_session=db_session
    )
    
    comment_service = providers.Factory(
        CommentService,
        comment_repo=comment_repository,
        post_repo=post_repository,
        user_repo=user_repository,
        db_session=db_session
    )