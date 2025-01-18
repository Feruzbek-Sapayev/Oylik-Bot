import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.database.models import async_main
from app.handlers.users import user
from aiogram.enums.parse_mode import ParseMode
from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(user)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')