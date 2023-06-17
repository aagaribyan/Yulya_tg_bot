LEXICON: dict[str, str] = \
    {
    '/start': '<b>Привет!</b>\n\n',
    '/help': '<b>Данный бот считывает только текстовые сообщения или файлы в формате .doc, '
             'присылает их перевод и сохраняет список использованных слов и их переводами</b>'
             'Для просмотра полного списка использованных слов используйте команду /list'
             'Для просмотра 10-и наиболее часто использованных слов используйте команду /frequent'
             'Для просмотра 10-ти наиболее редко использованных слов используйте команду /rare'
             'Для изменения целевого языка используйте команду /change',
    '/rare': 'Вывод 10-ти наиболее редко использованных слов',
    '/frequent': 'Вывод 10-ти наиболее часто использованных слов',
    '/change': 'Для изменения целевого языка перевода выберите язык из списка, '
               'либо самостоятельно введите код иного языка, список которых можно увидеть нажав "Все доступные языки"\n'
               '!Внимание!: изменение целевого языка приведет к удалению вашего словаря '
               'по текущему языку.\n'
               'Для возврата нажмите кнопку Отмена',

    'dict_save_ok': 'Словарь успешно сохранен',
    'dict_save_error': 'При сохранении словаря в файл возникла ошибка',
    'file_delete_ok': 'Файл удален',
    'file_not_found': 'Файла не найден на диске',

    'get_photo': 'Простите, я не поддерживаю работу с изображениями',
    'other_command': 'Простите, я не понимаю таких команд, пожалуйста напишите /help'
                     'чтобы узнать какие команды я знаю и что они делают, либо используйте Меню',
    'other_answer': 'Простите, я не умею обрабатывать сообщения данного типа ',

    'study_correct': 'Ответ правильный',
    'study_wrong': 'Ответ неверен, правильный ответ: ',
    'study_not_button': 'Для ответов, пожалуйста, используйте кнопки'
                        '\nЕсли хотите завершить обучение нажмите кнопку Завершить,'
                        'либо введите команду /endstudy',
    'cancel_study': 'Вы вышли из режима обучения, я снова буду переводить ваши текстовые сообщения и файлы '
                    'и запоминать переводы слов',

    'lang_change_ok': 'Язык успешно изменен',
    'lang_change_fail': 'При попытке изменения языка возникла ошибка, пожалуйста, обратитесь к авторам бота: '
                        '@armen_garibyan или @RomanovskayaJulia',  # + 'Текст ошибки: '?
    'all_langs': 'Все доступные языки',
    'cancel_lang': 'Изменение языка отменено',
    'wrong_lang_code': 'Указан неверный код языка, проверьте есть ли такой язык среди доступных нажав кнопку ""',

    'cancel': 'Завершить'
    }

# список кодов доступных языков для google translate
LEXICON_LANGS: dict[str, str] = \
    {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'Армянский',  # 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'Беларусский',  # 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'Английский',  # 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'Французский',  # 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'Итальянский',  # 'italian',
    'ja': 'Японский',  # 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'Русский',  # 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

# список основных языков для добавления в клавиатуру
LEXICON_MAIN_LANGS: list[str] = ['en', 'ru', 'fr', 'it', 'es', 'pt', 'de', 'hy']
