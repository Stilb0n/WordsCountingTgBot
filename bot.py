import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from app.database.models import async_main

from config import TOKEN


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)



# Регистрация роутера в диспетчере
dp.include_router(router)

# Запуск бота
async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
