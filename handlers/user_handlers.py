from copy import deepcopy
import docx

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.lexicon import LEXICON
from database.database import user_dict_template, users_db
from services.utils import (load_file_from_tg, save_dict_as_excel, translate_and_write_to_dict,
                            translate_all_text, delete_file_from_disk, choose_study_words)

import google.cloud.translate_v2 as translate
import os


# роутер aiogram
router: Router = Router()

# подключение переводчика
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/armen/Documents/Git Repos/Yulya_tg_bot/' \
                                               'western-dock-382910-f69f6855d1ba.json'
translate_client = translate.Client()

# инициализация хранилища (создание экземпляра класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()


# FSM класс для состояния обучения и состояния изменения целевого языка
class FSMMain(StatesGroup):
    study = State()  # состояние обучения
    # lang_change = State()  # состояние изменения языка (будет реализовано позже)


# хендлер команды /start
@router.message(CommandStart(), StateFilter(default_state))
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

'''
# хендлер команды /list
@router.message(Command(commands='list'), StateFilter(default_state))
async def process_list_command(message: Message):
    ans = ''
    for key, val in users_db[message.from_user.id]['words'].items():
        ans += str(key) + ': ' + str(val[0]) + '\n'
    
    # ans += '\n'
    # for key, val in users_db[message.from_user.id]['frequency'].items():
    #     ans += str(key) + ': ' + str(val) + '\n'

    await message.answer(text=ans)
'''


# хендлер команды /list (выдача списка всех слов) (при большом количестве плохо работает, подумать об отправке файла)
@router.message(Command(commands='list'), StateFilter(default_state))
async def process_list_command(message: Message):
    ans = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x: x[1])
    for key, val in sorted_freq:
        ans += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=ans)


# хендлер команды /rare (выдача самых редких слов)
@router.message(Command(commands='rare'), StateFilter(default_state))
async def process_rare_command(message: Message):
    ans = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x: x[1], reverse=False)
    for key, val in sorted_freq[:10]:
        ans += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=ans)


# хендлер команды /frequent (выдача самых частых слов)
@router.message(Command(commands='frequent'), StateFilter(default_state))
async def process_frequent_command(message: Message):
    ans = ''
    sorted_freq = sorted(users_db[message.from_user.id]['words'].items(), key=lambda x: x[1], reverse=True)
    for key, val in sorted_freq[:10]:
        ans += str(key) + ': ' + str(val[1]) + '\n'

    await message.answer(text=ans)


# хендлер команды /save (сохранение в excel файл (временная команда для тестов))
@router.message(Command(commands='save'), StateFilter(default_state))
async def process_save_command(message: Message):
    res = save_dict_as_excel(message.from_user.id)
    await message.answer(text=res)


# хендлер команды /delete (удаление файла)
@router.message(Command(commands='delete'), StateFilter(default_state))
async def process_delete_command(message: Message):
    res = delete_file_from_disk(message.from_user.id)
    await message.answer(text=res)


# Хэндлер на получение текстового сообщения (разбивает текст на отдельные слова и сохраняет их перевод)
# (плюс в ответ отправляет перевод текста в целом если чат не групповой)
@router.message(F.text, StateFilter(default_state))
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
# (пока реализовано только для .doc файла и есть вариант для .txt, остальные нужно доделать и разветвить)
@router.message(F.document, StateFilter(default_state))
async def process_document_message(message: Message):

    file_id = message.document.file_id
    file_on_disk = load_file_from_tg(file_id)

    # переделать под возможность чтения и txt
    # with open(file_on_disk, 'r', encoding='UTF-8') as file:
    #   text = file.read()

    # загрузка .doc файла
    doc = docx.Document(file_on_disk)  # ('file.doc')

    # чтение текста из файла
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text

    # добавление в словарь переводом отдельных слов
    await translate_and_write_to_dict(text, message.from_user.id)

    # запись в excel
    await save_dict_as_excel(message.from_user.id)

    # выбор рандомного слова из excel
    # df = pd.read_excel('database/xls/742654337.xlsx')
    # words = df['translate'].tolist()
    # random_word = random.choice(words)
    # await message.answer(random_word)


# хендлер команды /study (запуск состояния обучения)
@router.message(Command(commands='study'), StateFilter(default_state))
async def process_study_command(message: Message, state: FSMContext):
    # установка состояния обучения
    await state.set_state(FSMMain.study)

    # первое слово (следующие будут в process_study_word_chosen)
    markup, selected_word = choose_study_words(message.from_user.id)
    await message.answer(text='Для ответов используйте только кнопки! \nПервое слово: ' + selected_word,
                         reply_markup=markup)


# хендлер команды /cancel в состоянии обучения (выход из состояния обучения)
@router.message(StateFilter(FSMMain.study),
                Command(commands='cancel'))
async def process_cancel_study_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON['cancel_study'])


# хендлер для обработки ответа при обучении
@router.callback_query(StateFilter(FSMMain.study),
                       Text(text=['st_button1', 'st_button2', 'st_button3', 'st_button4', '_cancel_']))
async def process_study_word_chosen(callback: CallbackQuery, state: FSMContext):
    if callback.data == '_cancel_':
        # завершение обучения
        await state.clear()
    else:
        # проверка ответа пользователя
        user_id = callback.from_user.id
        correct_answer = users_db[user_id]['study_check']

        # перед проверкой подберем следующие слова
        markup, selected_word = choose_study_words(user_id)

        if callback.data[-1] == correct_answer[1]:
            # ответ верный
            ans = LEXICON['study_correct'] + '\nСледующее слово: ' + selected_word
        else:
            # ответ неправильный
            ans = LEXICON['study_wrong'] + correct_answer[0] + '\nСледующее слово: ' + selected_word

        # отправка ответа пользователю
        await callback.message.answer(text=ans,
                                      reply_markup=markup)


# хендлер для некорректного ввод в состоянии обучения
@router.message(StateFilter(FSMMain.study))
async def process_study_not_button(message: Message):
    await message.answer(text=LEXICON['study_not_button'])


# хендлер команды /change (создание клавиатуры со списком основных языков) (скорей всего стоит добавить FSM)
@router.message(Command(commands='change'), StateFilter(default_state))
async def process_change_command(message: Message):
    #
    #
    #
    await message.answer(text=LEXICON['/change'])
