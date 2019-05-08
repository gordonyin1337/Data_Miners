#Takes in a filename and takes a screenshot of the current screen, saving it
#in the same location as this file.

#python3 -m pip install Pillow
"""
from PIL import ImageGrab

def saveimg(name):
 #   im = ImageGrab.grab(bbox=(500, 500, 600, 700))
    im = ImageGrab.grab()
    im = im.convert("RGB")
    im.save(name + ".jpg")

saveimg("screenshot1")
"""

from PIL import ImageGrab
import win32gui

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def simg(name):
    win32gui.EnumWindows(enum_cb, toplist)

    program = [(hwnd, title) for hwnd, title in winlist if 'java' in title.lower()]
    program = program[0]
    hwnd = program[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    img = img.convert("RGB")
    img.save(name + ".jpg")

simg("screenshot1")
