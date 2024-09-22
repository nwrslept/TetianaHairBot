import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy


from dotenv import find_dotenv, load_dotenv

from midlewares.db import DataBaseSession
load_dotenv(find_dotenv())

from database.engine import create_db, drop_db, session_maker
from handlers.user_private import user_private_router
from handlers.admin_private import admin_router




bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


dp.include_router(user_private_router)
dp.include_router(admin_router)




async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()

async def on_shutdown(bot):
    print("Бот ліг")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())