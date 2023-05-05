import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import TOKEN
# from config.config_dev import TOKEN
from handlers import user_handlers, state_settings_handlers, state_forecast_handlers, admin_handlers
from handlers.entry_database import infinite_task
from keyboards.set_menu import set_menu

# Logger initialization
logger = logging.getLogger(__name__)


async def main():
    """
    Bot configuration and launch function
    """
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(state_settings_handlers.router)
    dp.include_router(state_forecast_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)

    await set_menu(bot)

    asyncio.create_task(infinite_task())

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        if __name__ == '__main__':
            asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # We print an error message to the console,
        # if a KeyboardInterrupt or SystemExit exception is received
        logger.error("Bot stopped!")
