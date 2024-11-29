import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import ContentType, Message

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
async def count_word_frequency(message: Message):
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
            # Не используем md.quote, заменяем на обычный вывод
            result = "\n".join([f"{word}: {count}" for word, count in word_count.items()])
            await message.answer(f"Частота слов в твоём сообщении:\n\n{result}")
        else:
            await message.answer("Кажется, в твоём сообщении нет слов для подсчёта.")
    except Exception as e:
        logging.error(f"Ошибка обработки сообщения: {e}")
        await message.answer("Произошла ошибка.")