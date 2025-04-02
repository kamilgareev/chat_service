from fastapi import FastAPI

from app.api.endpoints import users, chats, groups
from app.core.containers import Container


def create_app() -> FastAPI:
    app = FastAPI()

    container = Container()
    container.wire(modules=[chats, users, groups])

    app.container = container

    app.include_router(chats.router, prefix='/api/chats')
    app.include_router(users.router, prefix='/api/users')
    app.include_router(groups.router, prefix='/api/groups')

    return app

app = create_app()
