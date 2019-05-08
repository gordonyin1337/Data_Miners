#Takes in a filename and takes a screenshot of the current screen, saving it
#in the same location as this file.

#python3 -m pip install PIL OR python3 -m pip install Pillow

from PIL import ImageGrab

def saveimg(name):
 #   im = ImageGrab.grab(bbox=(500, 500, 600, 700))
    im = ImageGrab.grab()
    im = im.convert("RGB")
    im.save(name + ".jpg")

#saveimg("screenshot1")
