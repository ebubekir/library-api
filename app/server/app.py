from fastapi import FastAPI

from app.server.routes.books import router as BookRouter
from app.server.routes.user import router as UserRouter

app = FastAPI(debug=True)
app.include_router(BookRouter, tags=["Book"], prefix="/books")
app.include_router(UserRouter, tags=["User"], prefix="/users")


@app.get("/", tags=["Root"])
async def read_root():

    return {"message":"Welcome the fantastic app."}