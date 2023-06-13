from aiogram import Router, F
from aiogram.types import Message
from lexicon.lexicon import LEXICON

router: Router = Router()


# хендлер для ответа на изображение
@router.message(F.photo)
async def process_photo_answer(message: Message):
    await message.answer(text=LEXICON['get_photo'])


# хендлер для ответа на неизвестную команду
@router.message(F.text.startswith('/'))
async def process_other_command_answer(message: Message):
    await message.answer(text=LEXICON['other_command'])


# хендлер для сообщений, которые не попали в другие хендлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON['other_answer'])
