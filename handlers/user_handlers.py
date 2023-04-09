from copy import deepcopy
import docx

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.database import user_dict_template, users_db
from services.utils import load_file_from_tg, save_dict_as_excel, translate_and_write_to_dict, translate_text, delete_file_from_disk


# роутер aiogram
router: Router = Router()


# хендлер команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # добавление пользователя в user_db, если он новый
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

    '''
    # пока закомментирую, мешает
    file_name = 'database/xls/' + str(message.from_user.id) + '.xlsx'
    if os.path.exists(file_name):
        xls = pd.ExcelFile(file_name)
        users_db[message.from_user.id]['words'] = xls.parse(xls.sheet_names[0])
    '''

    await message.answer(text=LEXICON['/start'])


# хендлер команды /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# хендлер команды /list
@router.message(Command(commands='list'))
async def process_help_command(message: Message):
    answer_text = ''
    for key, val in users_db[message.from_user.id]['words'].items():
        answer_text += str(key) + ': ' + str(val[0]) + '\n'

    '''
    answer_text += '\n'
    for key, val in users_db[message.from_user.id]['frequency'].items():
        answer_text += str(key) + ': ' + str(val) + '\n'
    '''

    await message.answer(text=answer_text)


# хендлер команды /list2
@router.message(Command(commands='list2'))
async def process_help_command(message: Message):
    answer_text = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x:x[1])
    for key, val in sorted_freq:
        answer_text += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=answer_text)


# хендлер команды /save
@router.message(Command(commands='save'))
async def process_help_command(message: Message):
    res = save_dict_as_excel(message.from_user.id)
    await message.answer(text=res)


# хендлер команды /delete
@router.message(Command(commands='delete'))
async def process_help_command(message: Message):
    res = delete_file_from_disk(message.from_user.id)
    await message.answer(text=res)


# Хэндлер на получение текстового сообщения
@router.message(F.text)
async def process_text_message(message: Message):
    # общий перевод текста
    translation = translate_text()
    # отправка перевода пользователю
    await message.answer(text=translation)

    # добавление в словарь переводом отдельных слов
    translate_and_write_to_dict(message.text, message.from_user.id)

    # запись в excel
    save_dict_as_excel(message.from_user.id)


@router.message(F.document)
async def process_document_message(message: Message):

    file_id = message.document.file_id
    file_on_disk = load_file_from_tg(file_id)

    # переделать под возможность чтения и txt
    # with open(file_on_disk, 'r', encoding='UTF-8') as file:
    #   text = file.read()

    # загрузка .doc файла
    doc = docx.Document (file_on_disk) # ('file.doc')

    # чтение текста из файла
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text

    # добавление в словарь переводом отдельных слов
    translate_and_write_to_dict(text, message.from_user.id)

    # запись в excel
    save_dict_as_excel()

    # выбор рандомного слова из excel
    # df = pd.read_excel('database/xls/742654337.xlsx')
    # words = df['translate'].tolist()
    # random_word = random.choice(words)
    # await message.answer(random_word)
