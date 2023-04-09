import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers


# Инициализация логгера
logger = logging.getLogger(__name__)

# конфигурация логгирования
logging.basicConfig(level=logging.INFO,
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                           u'[%(asctime)s - %(name)s - %(message)s')

# вывод в консоль информации о начале запуска бота
logger.info('Starting bot')

# загрузка конфигураций в переменную config
config: Config = load_config()

# инициализация бота и диспетчера
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()


# функция конфигурации и запуска бота
async def main():
    # регистрация роуретов в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # пропуск накопившихся апдейтов и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        # запуск функции main в асинхронном режиме
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # вывод в консоль сообщения об ошибке при указанных исключениях
        logger.error('Bot stopped!')
