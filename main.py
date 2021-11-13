from config import BOT_TOKEN, TEST_TOKEN
import asyncio
from aiogram import Bot, Dispatcher, executor
import logging

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handlers import dp, send_to_admin, send_error
    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=send_error, skip_updates=True)
