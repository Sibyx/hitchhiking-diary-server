from fastapi import FastAPI

from hitchhiking_diary_server.rest.endpoints import tokens, users, photos, sync, status

app = FastAPI()

app.include_router(tokens.router, prefix="/api/v1", tags=["Tokens"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(photos.router, prefix="/api/v1", tags=["Photos"])
app.include_router(sync.router, prefix="/api/v1", tags=["Synchronization"])
app.include_router(status.router, prefix="/api/v1", tags=["Status"])
