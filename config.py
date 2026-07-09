version = '1.0.0.4-release'

import sys
from pathlib import Path


def _get_res_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def _get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


_res_dir = _get_res_dir() / 'data'
base_sql = str(_get_app_dir() / 'data' / 'events.db')


def data_path(filename):
    return (_res_dir / filename).as_posix()


get_event_period = 15