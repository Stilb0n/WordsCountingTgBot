import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import ContentType, Message
from app.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import app.keyboards as kb
import app.database.requests as rq

router = Router()

async def increment_request_count(user: User, session: AsyncSession):
    async with session.begin():
        user.request_count += 1
        await session.commit()

# Обработка команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply("Привет! Отправь мне текст, и я посчитаю частоту слов в нём.", reply_markup=kb.settings)

# Обработка текстовых сообщений для подсчёта частоты слов
@router.message(lambda msg: msg.content_type == ContentType.TEXT)
async def count_word_frequency(message: Message, session: AsyncSession, user: User):
    logging.info(f"User: {user.tg_id}, Session: {session}")
    try:
        text = message.text.lower()
        words = text.split()  # Разделение текста на слова
        word_count = {}

        # Подсчёт частоты слов
        for word in words:
            word = word.strip(",.!?()[]{}<>\"'")
            if word:
                word_count[word] = word_count.get(word, 0) + 1

        # Формирование ответа
        if word_count:
            result = "\n".join([f"{word}: {count}" for word, count in word_count.items()])
            await message.answer(f"Частота слов в твоём сообщении:\n\n{result}")
            user.request_count += 1 # увеличение счётчика запросов
            await session.commit() 
        else:
            await message.answer("Кажется, в твоём сообщении нет слов для подсчёта.")
    except Exception as e:
        logging.error(f"Ошибка обработки сообщения: {e}")
        await message.answer("Произошла ошибка.")