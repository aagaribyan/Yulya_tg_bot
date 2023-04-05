import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

from aiogram.filters import Command, CommandStart  # , Text
from aiogram.types import Message, ContentType
from lexicon.lexicon import LEXICON
from aiogram import F

# from aiogram import Router
# from handlers import other_handlers, user_handlers
# from keyboards.main_menu import set_main_menu
# from keyboards.pagination_kb import create_pagination_keyboard
# from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
# from services.file_handling import book
# from database.database import user_db, user_dict_template
# from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData


# Инициализация логгера
logger = logging.getLogger(__name__)

# router: Router = Router()

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


# хендлер команды /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    # добавление пользователя в user_db, если он новый
    # if message.from_user.id not in user_db:
    #    user_db[message.from_user.id] = deepcopy(user_dict_template)

    await message.answer(text=LEXICON['/start'])


# хендлер команды /help
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# Хэндлер на получение голосового и аудио сообщения
@dp.message(F.voice | F.audio | F.document)
async def process_voice_message(message: Message):
    '''
    Обработчик на получение голосового и аудио сообщения
    '''
    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    # file = await bot.get_file(file_id)
    # file_path = file.file_path
    # file_on_disk = f"{file_id}.tmp" # Path("", f"{file_id}.tmp")
    # await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено")

    #text = stt.audio_to_text(file_on_disk)
    #if not text:
    #    text = "Формат документа не поддерживается"
    #await message.answer(text)
    #
    #os.remove(file_on_disk)  # Удаление временного файла


# функция конфигурации и запуска бота
async def main():

    # настройка главного меню бота
    # await set_main_menu(bot)

    # регистрация роуретов в диспетчере
    # dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)

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
