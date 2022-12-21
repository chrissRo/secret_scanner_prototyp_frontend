from fastapi import FastAPI
from app.server.routes.findings_route import router as FindingRouter
from app.server.routes.user_route import router as UserRouter

app = FastAPI()

app.include_router(FindingRouter, tags=["Finding"], prefix='/finding')
app.include_router(UserRouter, tags=["User"], prefix='/user')

@app.get("/", tags=['root'])
async def root():
    return {"message": "Hello World"}
