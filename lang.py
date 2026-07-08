_current_lang = 'ru'

STRINGS = {
    'ru': {
        'calendar': 'Календарь событий',
        'settings': 'Настройки',
        'timezone': 'Часовой пояс',
        'language': 'Язык',
        'russian': 'Русский',
        'english': 'English',
        'donate': 'Задонатить',
        'exit_app': 'Выход',
        'notification': 'Уведомление',
        'auth_success': 'Успешная авторизация',
        'mute_title': 'Включен режим тишины',
        'mute_msg': 'Уведомления о новых событиях\n отключены до {mute_end}:00 утра',
        'reminder': 'Напоминание',
        'reminder_msg': 'Ближайшее событие сейчас уже начнётся',
        'event_going': 'Пойду',
        'event_not_going': 'Не пойду',
        'event_later': 'Решу позже',
        'donate_write': 'Написать',
        'donate_close': 'Закрыть',
        'calendar_close': 'Закрыть',
        'no_events': 'Событий нет',
        'email_copied': 'E-mail скопирован в буфер обмена',
        'silent_mode': 'Режим тишины',
        'start_hour': 'Начало',
        'end_hour': 'Конец',
        'reminder_setting': 'Напоминание',
        'minutes': 'мин',
    },
    'en': {
        'calendar': 'Event Calendar',
        'settings': 'Settings',
        'timezone': 'Timezone',
        'language': 'Language',
        'russian': 'Russian',
        'english': 'English',
        'donate': 'Donate',
        'exit_app': 'Exit',
        'notification': 'Notification',
        'auth_success': 'Authorization successful',
        'mute_title': 'Silent mode enabled',
        'mute_msg': 'Event notifications\ndisabled until {mute_end}:00',
        'reminder': 'Reminder',
        'reminder_msg': 'The nearest event is about to start',
        'event_going': "I'll go",
        'event_not_going': "Won't go",
        'event_later': 'Decide later',
        'donate_write': 'Write',
        'donate_close': 'Close',
        'calendar_close': 'Close',
        'no_events': 'No events',
        'email_copied': 'E-mail copied to clipboard',
        'silent_mode': 'Silent mode',
        'start_hour': 'Start',
        'end_hour': 'End',
        'reminder_setting': 'Reminder',
        'minutes': 'min',
    },
}


def _(key):
    return STRINGS[_current_lang].get(key, key)


def get_lang():
    return _current_lang


def set_lang(code):
    global _current_lang
    if code in STRINGS:
        _current_lang = code
