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
            logging.info("SessionMiddleware: сессия добавлена в data")
            return await handler(event, data)


from aiogram.types import Update, Message, CallbackQuery

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        session = data.get("session")
        if not session:
            logging.error("Session not found.")
            return await handler(event, data)

        # Логируем тип события
        logging.info(f"UserMiddleware: тип события {type(event)}")

        # Если событие — Update, извлекаем сообщение
        if isinstance(event, Update):
            if event.message:  # Если это сообщение
                tg_id = event.message.from_user.id
            elif event.callback_query:  # Если это callback_query (при необходимости)
                tg_id = event.callback_query.from_user.id
            else:
                logging.error("Unsupported update content.")
                return await handler(event, data)
        elif isinstance(event, Message):
            tg_id = event.from_user.id
        else:
            logging.error("Unsupported event type.")
            return await handler(event, data)

        # Получаем или создаём пользователя
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(tg_id=tg_id, request_count=0)
            session.add(user)
            await session.commit()

        data["user"] = user
        logging.info(f"UserMiddleware: добавлен пользователь {data['user']}")
        return await handler(event, data)