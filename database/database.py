# шаблон словаря со словами отдельного пользователя
user_dict_template = {'translate_to': 'en',  # целевой язык (может быть изменен пользователем)
                      'source_lang': 'ru',  # исходный язык
                      'words': {},  # словарь переводов использованных пользователем слов
                      'study_check': []  # вспомогательный список для состояния обучения
                      }

# инициализация базы данных
users_db = {}
