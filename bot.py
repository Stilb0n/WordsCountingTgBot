import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from app.database.models import async_main
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import TOKEN

async def register_user(tg_id: int, session: AsyncSession):
    async with session.begin():
        # Проверяем, существует ли пользователь
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        
        if user is None:
            # Создаем нового пользователя, если он не найден
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()
            print(f"Пользователь с ID {tg_id} зарегистрирован.")
        else:
            print(f"Пользователь с ID {tg_id} уже существует.")

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
