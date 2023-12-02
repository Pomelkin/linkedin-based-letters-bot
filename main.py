from aiogram import Bot, Dispatcher
from core.config import TELEGRAM_TOKEN
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from core.loader import dp, bot
import asyncio
import logging

TELEGRAM_API_KEY = TELEGRAM_TOKEN


async def start_bot():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())
