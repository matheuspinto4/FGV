import numpy as np
import win32gui
from mss import mss

class WindowCapture:
    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Janela "{window_name}" não encontrada.')

        self.sct = mss()

    def get_screenshot(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bottom = rect

        monitor = {
            "top": top,
            "left": left,
            "width": right - left,
            "height": bottom - top,
        }

        # A biblioteca mss retorna uma imagem com 4 canais (RGBA),
        # por isso, convertemos para 3 canais (RGB) com NumPy
        img = np.array(self.sct.grab(monitor))
        return img[:, :, :3]