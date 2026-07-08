from Imports import *
from lang import _, get_lang, set_lang


class Tray:
    GMT_CITIES = {
        -12: "о. Бейкер", -11: "о. Мидуэй, Апиа",
        -10: "Гавайи, Папеэте", -9: "Аляска, Анкоридж",
        -8: "Лос-Анджелес, Ванкувер", -7: "Денвер, Калгари",
        -6: "Чикаго, Мехико", -5: "Нью-Йорк, Торонто, Богота",
        -4: "Каракас, Сантьяго", -3: "Бразилия, Буэнос-Айрес",
        -2: "Средне-Атлантический", -1: "Азорские о-ва, Прая",
        0: "Лондон, Дублин, Лиссабон", 1: "Париж, Рим, Берлин",
        2: "Калининград", 3: "Москва, Санкт-Петербург, Стамбул",
        4: "Самара, Казань", 5: "Екатеринбург, Челябинск",
        6: "Омск", 7: "Новосибирск, Красноярск, Бангкок",
        8: "Иркутск", 9: "Якутск",
        10: "Владивосток, Хабаровск", 11: "Магадан",
        12: "Камчатка", 13: "Нукуалофа",
        14: "Кирибати",
    }

    def __init__(self, icon):
        self.icon = icon

    def tray_menu(self):
        self.menu = QMenu()

        self.vers_action = QAction(version)
        self.vers_action.setEnabled(False)
        self.menu.addAction(self.vers_action)

        self.calendar_action = QAction(_('calendar'), triggered=self.show_calendar)
        self.menu.addAction(self.calendar_action)

        self.settings_menu = self.menu.addMenu(_('settings'))
        self.tz_menu = self.settings_menu.addMenu(_('timezone'))
        self.timezone_actions = []
        current_gmt = self.database.gmt
        for offset in range(-12, 15):
            city = self.GMT_CITIES.get(offset, "")
            label = f"UTC{offset:+d}  {city}" if city else f"UTC{offset:+d}"
            action = QAction(label, checkable=True)
            action.setData(offset)
            action.setChecked(offset == current_gmt)
            action.triggered.connect(lambda checked, o=offset: self._set_timezone(o))
            self.tz_menu.addAction(action)
            self.timezone_actions.append(action)

        self.lang_menu = self.settings_menu.addMenu(_('language'))
        self.lang_actions = []
        current_lang = get_lang()
        for code, key in [('ru', 'russian'), ('en', 'english')]:
            action = QAction(_(key), checkable=True)
            action.setData(code)
            action.setChecked(code == current_lang)
            action.triggered.connect(lambda checked, l=code: self._set_language(l))
            self.lang_menu.addAction(action)
            self.lang_actions.append(action)

        self.silent_menu = self.settings_menu.addMenu(_('silent_mode'))
        self.silent_start_menu = self.silent_menu.addMenu(_('start_hour'))
        self.silent_end_menu = self.silent_menu.addMenu(_('end_hour'))

        self.silent_start_actions = []
        self.silent_end_actions = []
        current_start = self.database.mute_start
        current_end = self.database.mute_end
        for hour in range(24):
            label = f"{hour:02d}:00"
            act_s = QAction(label, checkable=True)
            act_s.setData(hour)
            act_s.setChecked(hour == current_start)
            act_s.triggered.connect(lambda checked, h=hour: self._set_silent_hour('mute_start', h))
            self.silent_start_menu.addAction(act_s)
            self.silent_start_actions.append(act_s)

            act_e = QAction(label, checkable=True)
            act_e.setData(hour)
            act_e.setChecked(hour == current_end)
            act_e.triggered.connect(lambda checked, h=hour: self._set_silent_hour('mute_end', h))
            self.silent_end_menu.addAction(act_e)
            self.silent_end_actions.append(act_e)

        self.reminder_menu = self.settings_menu.addMenu(_('reminder_setting'))
        self.reminder_actions = []
        current_notify = self.database.notify_time
        for minutes in [1, 5, 10, 15, 30]:
            action = QAction(f"{minutes} {_('minutes')}", checkable=True)
            action.setData(minutes)
            action.setChecked(minutes == current_notify)
            action.triggered.connect(lambda checked, m=minutes: self._set_remind_time(m))
            self.reminder_menu.addAction(action)
            self.reminder_actions.append(action)

        self.donate_action = QAction(_('donate'), triggered=self.show_donate)
        self.exit_action = QAction(_('exit_app'), triggered=self.exit_action_func)
        self.menu.addAction(self.donate_action)
        self.menu.addAction(self.exit_action)

        self.tr.icon.setContextMenu(self.menu)
        self.tr.icon.show()

    def _set_timezone(self, offset):
        for action in self.timezone_actions:
            action.setChecked(action.data() == offset)
        self.database.set_setting('gmt', offset)
        self.database.gmt = offset

    def _set_language(self, code):
        set_lang(code)
        self.database.set_setting('lang', code)
        self._refresh_menu_texts()

    def _refresh_menu_texts(self):
        self.calendar_action.setText(_('calendar'))
        self.settings_menu.setTitle(_('settings'))
        self.tz_menu.setTitle(_('timezone'))
        self.lang_menu.setTitle(_('language'))
        self.silent_menu.setTitle(_('silent_mode'))
        self.silent_start_menu.setTitle(_('start_hour'))
        self.silent_end_menu.setTitle(_('end_hour'))
        self.reminder_menu.setTitle(_('reminder_setting'))
        for action in self.reminder_actions:
            action.setText(f"{action.data()} {_('minutes')}")
        self.donate_action.setText(_('donate'))
        self.exit_action.setText(_('exit_app'))
        current_lang = get_lang()
        for action in self.lang_actions:
            code = action.data()
            action.setText(_('russian') if code == 'ru' else _('english'))
            action.setChecked(code == current_lang)

    def _set_silent_hour(self, setting, hour):
        if setting == 'mute_start':
            self.database.mute_start = hour
            for a in self.silent_start_actions:
                a.setChecked(a.data() == hour)
        else:
            self.database.mute_end = hour
            for a in self.silent_end_actions:
                a.setChecked(a.data() == hour)
        self.database.set_setting(setting, hour)

    def _set_remind_time(self, minutes):
        for action in self.reminder_actions:
            action.setChecked(action.data() == minutes)
        self.database.set_setting('notify_time', minutes)
        self.database.notify_time = minutes