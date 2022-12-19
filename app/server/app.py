from fastapi import FastAPI
from app.server.routes.findings_route import router as FindingRouter

app = FastAPI()

app.include_router(FindingRouter, tags=["Finding"], prefix='/finding')

@app.get("/", tags=['root'])
async def root():
    return {"message": "Hello World"}
