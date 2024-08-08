from Imports import *

class Tray:
    def __init__(self, icon):
        self.icon = icon

    def tray_menu(self):
        self.menu = QMenu()
        self.vers_action = QAction(version)
        self.vers_action.setEnabled(False)
        self.settings_action = QAction("Настройки", triggered=self.settings_action_func)
        self.donate_action = QAction("Задонатить", triggered=self.show_donate)
        self.settings_action.setEnabled(False)
        self.exit_action = QAction("Выход", triggered=self.exit_action_func)
        self.menu.addAction(self.vers_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.donate_action)
        self.menu.addAction(self.exit_action)
        self.tr.icon.setContextMenu(self.menu)
        self.tr.icon.show()