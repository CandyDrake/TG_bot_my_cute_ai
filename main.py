
from aiogram import Dispatcher
from dotenv import load_dotenv

from database.models import async_main
from database.users import *
from handlers.handlers import router
from api.api import check_and_send


async def bot_start_work_message(bot: Bot, user_ids):
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, 'Я отключался, но сейчас снова здесь!')
            await asyncio.sleep(1)
        except Exception:
            print('не удалось отправить сообщение')


async def main():
    load_dotenv()
    await async_main()
    async with Bot(token=os.getenv('BOT_TOKEN')) as bot:
        dp = Dispatcher()
        dp.include_router(router)
        user_ids = load_user_ids()
        if user_ids:
            await bot_start_work_message(bot, user_ids)
        asyncio.create_task(check_and_send(bot))

        await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print('Бот выключен')
