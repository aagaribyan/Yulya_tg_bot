import pandas as pd
import google.cloud.translate_v2 as translate
import os
from random import randint

from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import Config, load_config
from database.database import users_db
from lexicon.lexicon import LEXICON

# загрузка конфигураций в переменную config
config: Config = load_config()

# инициализация бота и диспетчера
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

# подключение переводчика
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/armen/Documents/Git Repos/Yulya_tg_bot/western-dock-382910-f69f6855d1ba.json'
translate_client = translate.Client()


async def translate_all_text(text, user_id):
    target = users_db[user_id]['translate_to']
    source = users_db[user_id]['source_lang']

    # общий перевод текста
    translation = translate_client.translate(text, source_language=source, target_language=target)
    return translation


# перевод и запись в словарь
async def translate_and_write_to_dict(text, user_id):
    target = users_db[user_id]['translate_to']
    source = users_db[user_id]['source_lang']

    for i in '''!()-–[]{};?@#$%:'"\,./^&amp;*_''':
        text = text.replace(i, "")

    # добавление в словарь переводом отдельных слов
    for split_inp in text.split():
        translation = translate_client.translate(split_inp.lower(), source_language=source, target_language=target)

        trans_text = translation['translatedText'].lower()
        words_dict = users_db[user_id]['words']

        words_dict.setdefault(trans_text, [split_inp.lower(), 0])
        words_dict[trans_text][1] += 1

    # return translation


# получение файла из телеграма по id и сообщения
async def load_file_from_tg(file_id):
    file = await bot.get_file(file_id)

    file_path = file.file_path
    file_on_disk = f"C:/Users/armen/Documents/Git Repos/Yulya_tg_bot/database/loaded_files/{file_id}.tmp"

    await bot.download_file(file_path, destination=file_on_disk)
    # await message.reply("Документ получен")

    return file_on_disk


# сохранения состояния словаря отдельного пользователя в excel файл
async def save_dict_as_excel(user_id):
    try:
        # переводим в формат pandas датафрейма
        df = pd.DataFrame(users_db[user_id]['words'], index=['translate', 'frequency']).T

        # сортируем по частоте появлений
        df.sort_values(by=['frequency'], ascending=[False])

        # сохраняем в файл
        df.to_excel('database/xls/' + str(user_id) + '.xlsx')  # , index=[0])

        return LEXICON['dict_save_ok']

    except:
        return LEXICON['dict_save_error']


# удаление файла со словарем пользователя с диска
async def delete_file_from_disk(user_id):
    try:
        os.remove('database/xls/' + str(user_id) + '.xlsx')
        return LEXICON['file_delete_ok']
    except FileNotFoundError:
        return LEXICON['file_not_found']


# фунция подбора 4-х случайных слов из словаря пользователя
def choose_study_words(user_id):
    words = users_db[user_id]  # dict со словами вида 'перевод': ['изначальное_слово', кол-во_появления]

    # инициализация билдера
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # инициализация списка для кнопок
    buttons: list[InlineKeyboardButton] = []

    # подбор слов (пока сделаю равновероятный вариант)
    chosen = []
    i = 1
    while len(buttons) < 4:
        random_word = ...  # подбор рандомного элемента (ключа словаря), подзабыл какая для этого была ф-ция
        if random_word not in chosen:
            chosen.append(random_word)
            buttons.append(InlineKeyboardButton(text=words[random_word][0],
                                                callback_data='st_button'+str(i)))
            i += 1

    # последняя кнопка для прекращения обучения (выхода из соответствующего состояния)
    buttons.append(InlineKeyboardButton(text=LEXICON['cancel'],
                                        callback_data='_end_'))
    # создание клавиатуры
    kb_builder.row(*buttons, width=2)
    markup = kb_builder.as_markup()

    # выбор слова для перевода пользователем
    ind = randint(0, 4)
    selected_word = chosen[ind]
    # запись правильного ответа в базу данному пользователю
    users_db[user_id]['study_check'] = [words[selected_word][0], str(ind+1)]

    return markup, selected_word
