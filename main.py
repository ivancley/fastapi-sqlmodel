from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.v1.database import create_db_and_tables 
from app.v1.context.controllers import router as context_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database created")
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(context_router)

@app.get("/status")
def status():
    return {"status": "ok"}