import logging
from aiogram.types import Message, CallbackQuery
from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from sqlalchemy.future import select
from app.database.models import User
class SessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with self.session_factory() as session:
            data["session"] = session
            return await handler(event, data)


class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        session = data.get("session")  # Получаем сессию
        if not session:
            return await handler(event, data)

        tg_id = None
        if isinstance(event, Message):
            tg_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            tg_id = event.from_user.id

        if not tg_id:
            return await handler(event, data)

        # Получаем пользователя из базы
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        # Если пользователь не найден, создаём его
        if not user:
            user = User(tg_id=tg_id, request_count=0)
            session.add(user)
            await session.commit()

        # Добавляем пользователя в data
        logging.info(f"User found or created: {user.tg_id}")
        data["user"] = user
        return await handler(event, data)