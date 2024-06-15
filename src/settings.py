import os

# DIRS

BASE_DIR = os.getcwd()

# WINDOW

W_SIZE = (1000, 600)

FPS = -1

# MONITOR

from screeninfo import get_monitors

MONITOR_DPI = -1
for m in get_monitors():
    if m.is_primary:
        MONITOR_DPI = m.width / m.width_mm * 25.4