from fastapi import FastAPI
from infrastructure.container import Container
from infrastructure.api.routers import post_router, user_router, comment_router
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Blog API",
        description="API",
        version="1.0.0"
    )
    
    # DI контейнер
    container = Container()
    container.wire(modules=[
        "infrastructure.api.routers.post_router",
        "infrastructure.api.routers.user_router",
        "infrastructure.api.routers.comment_router"
    ])
    app.container = container

    app.include_router(post_router.router)
    app.include_router(user_router.router)
    app.include_router(comment_router.router)

    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

    return app

app = create_app()

@app.get("/")
def read_root():
    return {"message": "API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)