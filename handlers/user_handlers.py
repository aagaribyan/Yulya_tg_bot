from copy import deepcopy
import docx

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from database.database import user_dict_template, users_db
from services.utils import load_file_from_tg, save_dict_as_excel, translate_and_write_to_dict, translate_all_text, delete_file_from_disk

import google.cloud.translate_v2 as translate
import os


# роутер aiogram
router: Router = Router()


# подключение переводчика
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/armen/Documents/Git Repos/Yulya_tg_bot/western-dock-382910-f69f6855d1ba.json'
translate_client = translate.Client()


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
async def process_list_command(message: Message):
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
async def process_lsit2_command(message: Message):
    answer_text = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x:x[1])
    for key, val in sorted_freq:
        answer_text += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=answer_text)


# хендлер команды /rare
@router.message(Command(commands='rare'))
async def process_rare_command(message: Message):
    answer_text = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x: x[1], reverse=False)
    for key, val in sorted_freq[:10]:
        answer_text += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=answer_text)


# хендлер команды /frequent
@router.message(Command(commands='frequent'))
async def process_frequent_command(message: Message):
    answer_text = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x: x[1], reverse=True)
    for key, val in sorted_freq[:10]:
        answer_text += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=answer_text)


# хендлер команды /save
# сохранение в excel файл (временная команда для тестов)
@router.message(Command(commands='save'))
async def process_save_command(message: Message):
    res = save_dict_as_excel(message.from_user.id)
    await message.answer(text=res)


# хендлер команды /delete
# команда для удаления файла
@router.message(Command(commands='delete'))
async def process_delete_command(message: Message):
    res = delete_file_from_disk(message.from_user.id)
    await message.answer(text=res)


# Хэндлер на получение текстового сообщения
# разбивает текст на отдельные слова и сохраняет их перевод
# (плюс в ответ отправляет перевод текста в целом если чат не групповой)
@router.message(F.text)
async def process_text_message(message: Message):
    target = users_db[message.from_user.id]['translate_to']
    source = users_db[message.from_user.id]['source_lang']

    # общий перевод текста
    translation = translate_client.translate(message.text, source_language=source, target_language=target)

    # общий перевод текста
    # translation = translate_all_text(message.text, message.from_user.id)
    # print(translation['translatedText'])

    # проверка, что чат не групповой
    if message.chat.id == message.from_user.id:
        # отправка перевода пользователю
        await message.answer(text=translation['translatedText'])  # text=translation)

    # добавление в словарь переводом отдельных слов
    await translate_and_write_to_dict(message.text, message.from_user.id)

    # запись в excel
    await save_dict_as_excel(message.from_user.id)


# хендлер на получение документа
# (пока реализовано только для .doc файла и есть вариант для .txt, остальные нужно доделать)
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
    await translate_and_write_to_dict(text, message.from_user.id)

    # запись в excel
    await save_dict_as_excel()

    # выбор рандомного слова из excel
    # df = pd.read_excel('database/xls/742654337.xlsx')
    # words = df['translate'].tolist()
    # random_word = random.choice(words)
    # await message.answer(random_word)
