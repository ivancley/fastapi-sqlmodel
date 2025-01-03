from fastapi import APIRouter, Depends
from typing import List
from app.v1.context.schemas import ContextCreate, ContextRead, ContextUpdate
from app.v1.context.services import ContextService
from app.v1.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/api/v1/contextos",
    tags=["Contextos"],
)

context_service = ContextService()

@router.post("/", response_model=ContextRead)
async def create_context(context: ContextCreate, session: AsyncSession = Depends(get_session)):
    return await context_service.create_context(session, context)

@router.get("/", response_model=List[ContextRead])
async def get_all_contexts(session: AsyncSession = Depends(get_session)):
    return await context_service.get_all_contexts(session)

@router.get("/{id}", response_model=ContextRead)
async def get_context(id: str, session: AsyncSession = Depends(get_session)):
    return await context_service.get_context_by_id(session, id)

@router.put("/{id}", response_model=ContextRead)
async def update_context(id: str, context: ContextUpdate, session: AsyncSession = Depends(get_session)):
    return await context_service.update_context(session, id, context)

@router.delete("/{id}", response_model=ContextRead)
async def delete_context(id: str, session: AsyncSession = Depends(get_session)):
    return await context_service.delete_context(session, id )