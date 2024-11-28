import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import ContentType, Message
from aiogram.utils import markdown as md
from config import TOKEN


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
router = Router()
dp = Dispatcher(storage=storage)

# Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь мне текст, и я посчитаю частоту слов в нём.")

# Обработка текстовых сообщений для подсчёта частоты слов
@dp.message(lambda msg: msg.content_type == ContentType.TEXT)
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

# Регистрация роутера в диспетчере
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
