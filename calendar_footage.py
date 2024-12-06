import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from datetime import datetime

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Календарь событий")
        self.setGeometry(760, 400, 480, 480)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Создание календаря
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_events)

        # Убираем номера недель
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setObjectName("calendar")

        # Устанавливаем стиль для календаря
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: transparent;
            }
            #calendar QWidget {
                alternate-background-color: #70a3d2;
            }
            #qt_calendar_navigationbar {
                background-color: #70a3d2;
                border-bottom: 2px solid transparent;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                min-height: 32px;
                max-height: 32px;
            }
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                border: none;
                qproperty-icon: none;
                background-color: transparent;
                padding: 5px;
            }
            #qt_calendar_prevmonth {
                margin-left: 15px;
                image: url('data/arrLeft.png');
            }
            #qt_calendar_nextmonth {
                margin-right: 15px;
                image: url('data/arrRight.png')
            }
            #qt_calendar_yearbutton {
                font-size: 14px;
                margin: 8px;
            }
            #qt_calendar_monthbutton {
                font-size: 12px;
            }
            #qt_calendar_yearedit {
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                min-width: 53px;
                max-height: 30px;
                padding: 0px 3px;
            }
            #qt_calendar_calendarview {
                border-bottom: 2px solid transparent;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            #qt_calendar_calendarview::item:focus {
                background-color: #70a3d2;
                border: 2px solid #fff;
                border-radius: 5px;
                color: #fff;
                font-weight: bold;
            }
        """)

        self.event_display = QPlainTextEdit(self)
        self.event_display.setReadOnly(True)
        self.event_display.setStyleSheet("""
            QPlainTextEdit {
                height: 90px;
                min-height: 90px;
                max-height: 150px;
                font-size: 14px;
                color: #000;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: rgba(255,255,255,0.9);
                border: none; /* Убираем рамку */
            }
        """)

        # Применяем размытие
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(50)  # Установите радиус размытия
        self.event_display.setGraphicsEffect(blur_effect)

        layout = QVBoxLayout()
        layout.setSpacing(1)
        layout.addWidget(self.calendar)
        layout.addWidget(self.event_display)

        self.button = QPushButton("Закрыть")
        self.button.setObjectName("btn_close")
        self.button.setStyleSheet("""
            QPushButton#btn_close {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 8px 6px;
                margin-top: 3px;
            }
        
            QPushButton#btn_close:hover {
                background-color: #6CBFD4;
            }
        """)

        self.button.clicked.connect(self.close)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Пример событий
        self.events = {
            datetime(2024, 12, 15): [
                "1. 14:00-16:00 (17 этаж)",
                "2. 18:00-19:00 (20 этаж)"
            ],
            datetime(2024, 12, 16): [
                "1. 10:00-11:00 (1 этаж)",
                "2. 12:00-13:00 (2 этаж)"
            ]
        }

        # Выделяем сегодняшнюю дату
        self.highlight_today()
        # Выделяем определенные даты
        self.highlight_specific_date(QDate(2024, 12, 15))
        self.highlight_specific_date(QDate(2024, 12, 16))

    def highlight_specific_date(self, date):
        # Установка формата текста для определенной даты
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor(113, 246, 192)))  # Установить цвет фона
        format.setForeground(QBrush(QColor(255, 255, 255)))  # Установить цвет шрифта
        self.calendar.setDateTextFormat(date, format)

    def highlight_today(self):
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.calendar.setCurrentPage(today.year(), today.month())

    def show_events(self, date):
        # Получаем дату из QDate
        selected_date = datetime(date.year(), date.month(), date.day())
        self.event_display.clear()
        if selected_date in self.events:
            events = "\n".join(self.events[selected_date])
            self.event_display.setPlainText(events)
        else:
            self.event_display.setPlainText("Событий нет")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())