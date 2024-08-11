# конфиг
from config import *

# модули
import sys
# import platform
import os
import subprocess
import json
import traceback
import threading
import time
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import pyaudio
import wave

# try:
#     import winsound
# except ImportError:
#     from playsound import playsound
import webbrowser
import base64
import pyperclip

# классы
from Encryption import *
from Database import *
from Auth import *
from Tray import *
from CustomWindows import *
from Event import *
from Audio import *