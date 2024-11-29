import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import ContentType, Message
from sqlalchemy import select
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import app.keyboards as kb
import app.database.requests as rq

router = Router()



# Обработка команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply("Привет! Отправь мне текст, и я посчитаю частоту слов в нём.", reply_markup=kb.settings)


# Обработка текстовых сообщений для подсчёта частоты слов
@router.message(lambda msg: msg.content_type == ContentType.TEXT)
async def count_word_frequency(message: Message, **kwargs):
    session = kwargs.get("session")
    tg_id = message.from_user.id
    
    # Извлечение пользователя из базы
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(tg_id=tg_id, request_count=1)  # Начинаем с 1, если новый пользователь
        session.add(user)
    else:
        user.request_count += 1  # Увеличиваем счетчик для существующего пользователя

    await session.commit()  # Сохраняем изменения в базе

    await message.answer(f"Пользователь: {user.tg_id}, запросов: {user.request_count}")