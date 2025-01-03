from typing import List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.decorators import handle_sqlalchemy_errors_async
from app.v1.models import ContextModel
from app.v1.context.schemas import ContextCreate, ContextUpdate
from app.core.exceptions import ExceptionNotFound


class ContextService:

    def _not_deleted(self):
        return select(ContextModel).where(ContextModel.is_deleted == False)

    async def _save_and_refresh(
        self, session: AsyncSession, instance: ContextModel
    ) -> ContextModel:
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
    
    async def _get_context_or_404(
        self, session: AsyncSession, context_id: str
    ) -> ContextModel:
        query = self._not_deleted().where(ContextModel.id == context_id)
        result = await session.execute(query)
        context = result.scalars().first()
        if not context:
            raise ExceptionNotFound(detail="Contexto não encontrado")
        return context
    
    @handle_sqlalchemy_errors_async
    async def get_all_contexts(self, session: AsyncSession) -> list[ContextModel]:
        result = await session.execute(self._not_deleted())
        return result.scalars().all()

    @handle_sqlalchemy_errors_async
    async def get_context_by_id(
        self, session: AsyncSession, context_id: str,
    ) -> ContextModel:
        return await self._get_context_or_404(session, context_id)

    @handle_sqlalchemy_errors_async
    async def create_context(
        self, session: AsyncSession, context: ContextCreate,
    ) -> ContextModel:
        context_model = ContextModel(name=context.name)
        return await self._save_and_refresh(session, context_model)
    
    
    @handle_sqlalchemy_errors_async
    async def update_context(
        self, session: AsyncSession, context_id: str, context_update: ContextUpdate
    ) -> ContextModel:
        context_db = await self._get_context_or_404(session, context_id)
        for key, value in context_update.dict(exclude_unset=True).items():
            setattr(context_db, key, value)
        return await self._save_and_refresh(session, context_db)

    @handle_sqlalchemy_errors_async
    async def delete_context(
        self, session: AsyncSession,  context_id: str,
    ) -> ContextModel:
        context_db = await self._get_context_or_404(session, context_id)
        context_db.is_deleted = True
        return await self._save_and_refresh(session, context_db)
