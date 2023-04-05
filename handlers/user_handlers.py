'''
from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, ContentType
from lexicon.lexicon import LEXICON
from aiogram import F
# from keyboards.pagination_kb import create_pagination_keyboard
# from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
# from services.file_handling import book
# from database.database import user_db, user_dict_template
# from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData

router: Router = Router()


# хендлер команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # добавление пользователя в user_db, если он новый
    # if message.from_user.id not in user_db:
    #    user_db[message.from_user.id] = deepcopy(user_dict_template)

    await message.answer(text=LEXICON['/start'])


# хендлер команды /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# Хэндлер на получение голосового и аудио сообщения
@router.message(content_types=[
    ContentType.VOICE,
    ContentType.AUDIO,
    ContentType.DOCUMENT
    ]
)
async def voice_message_handler(message: Message):
    """
    Обработчик на получение голосового и аудио сообщения
    """
    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено")

    text = stt.audio_to_text(file_on_disk)
    if not text:
        text = "Формат документа не поддерживается"
    await message.answer(text)

    os.remove(file_on_disk)  # Удаление временного файла
'''


'''
# хендлер команды /bookmarks (показ закладок)
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if user_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(*user_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

# хендлер команды /beginning (переход в начало книги)
@router.message(Command(commands='beginning'))
async def process_beginnig_command(message: Message):
    if message.from_user.id not in user_db:  # на всякий случай
        user_db[message.from_user.id] = deepcopy(user_dict_template)

    # переводим указатель этого пользователя в нашей "базе" на страницу 1
    user_db[message.from_user.id]['page'] = 1

    text = book[user_db[message.from_user.id]['page']]
    pag_kb = create_pagination_keyboard('backward', f'1/{len(book)}', 'forward')

    # выводим первую страницу и клавиатуру перехода по страницам
    await message.answer(text=text, reply_markup=pag_kb)

# хендлер команды /continue (продолжение чтения)
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[user_db[message.from_user.id]['page']]
    pag_kb = create_pagination_keyboard('backward', f'{user_db[message.from_user.id]["page"]}/{len(book)}', 'forward')

    # отображаем страницу, на которой остановился пользователь и клавиатуру перехода по страницам
    await message.answer(text=text, reply_markup=pag_kb)

# хендлер перехода на следующую страницу
@router.callback_query(Text(text='forward'))
async def process_next_page(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(book):
        user_db[callback.from_user.id]['page'] += 1
        text = book[user_db[callback.from_user.id]['page']]
        pag_kb = create_pagination_keyboard('backward', 
                                            f'{user_db[callback.from_user.id]["page"]}/{len(book)}', 'forward')

        await callback.message.edit_text(text=text, reply_markup=pag_kb)

    await callback.answer()


# хендлер перехода на предыдущую страницу
@router.callback_query(Text(text='backward'))
async def process_previous_page(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        pag_kb = create_pagination_keyboard('backward', 
                                            f'{user_db[callback.from_user.id]["page"]}/{len(book)}','forward')

        await callback.message.edit_text(text=text, reply_markup=pag_kb)

    await callback.answer()

# хендлер для инлайн-кнопки с номером текущей страницы (добавление закладки)
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].add(user_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки')

# хендлер выбора закладки из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['page'] = int(callback.data)
    text = book[int(callback.data)]
    pag_kb = create_pagination_keyboard('backward', f'{int(callback.data)}/{len(book)}','forward')

    await callback.message.edit_text(text=text, reply_markup=pag_kb)
    await callback.answer()

# хендлер нажатия кнопки "Редактировать" на списке закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data],
                                     reply_markup=create_edit_keyboard(*user_db[callback.from_user.id]['bookmarks']))
    await callback.answer()

# хендлер нажатия кнопки "отменить" под списком закладок
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()

# хендлер выбора закладки из списка редактирования (удаления) закладок
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    # если ещё остались закладки, отображаем клавиатуру редактирования с оставшимися закладками
    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'],
                                         reply_markup=create_edit_keyboard(*user_db[callback.from_user.id]['bookmarks']))
    # иначе отписываемся что закладок не осталось
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])

    await callback.answer()
'''