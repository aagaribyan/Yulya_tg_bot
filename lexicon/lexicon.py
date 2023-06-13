LEXICON: dict[str, str] = {'/start': '<b>Привет!</b>\n\n',
                           '/help': '<b>Данный бот считывает только текстовые сообщения или файлы в формате .doc, '
                                    'присылает их перевод и сохраянет список использованых слов и их переводами</b>',
                           '/rare': 'Вывод 10-ти наиболее редко использованных слов',
                           '/frequent': 'Вывод 10-ти наиболее часто использованных слов',

                           'dict_save_ok': 'Словарь успешно сохранен',
                           'dict_save_error': 'При сохранении словаря в файл возникла ошибка',
                           'file_delete_ok': 'Файл удален',
                           'file_not_found': 'Файла не найден на диске',

                           'get_photo': 'Простите, я не поддерживаю работу с изображениями',
                           'other_command': 'Простите, я не понимаю таких команд, пожалуйста напишите /help'
                                           'чтобы узнать какие команды я знаю и что они делают, либо используйте Меню',
                           'other_answer': 'Простите, я не умею обрабатывать сообщения данного типа ',
                           }

LEXICON_COMMANDS: dict[str, str] = \
    {'/help': 'Справка по работе бота'
              'Для просмотра полного списка использованных слов используте команду /list'
              'Для просмотра 10-и наиобее часто использованных слов используйте команду /frequent'
              'Для просмотра 10-ти наиболее редко использованных слов используйте команду /rare'

    }