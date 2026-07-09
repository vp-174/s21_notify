version = '1.0.0.4-release'

import os
import sys

def _get_res_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def _get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

_res_dir = os.path.join(_get_res_dir(), 'data').replace('\\', '/')
base_sql = os.path.join(_get_app_dir(), 'data', 'events.db')

def data_path(filename):
    return os.path.join(_res_dir, filename)

# Период опроса сервера в минутах
get_event_period = 15