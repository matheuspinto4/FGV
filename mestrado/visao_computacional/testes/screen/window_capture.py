import numpy as np
import win32gui
import time
from mss import mss

class WindowCapture:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.sct = mss()

        try:
            win32gui.SetForegroundWindow(self.hwnd)
            time.sleep(0.5)
        except Exception as e:
            print(f"Não foi possível definir a janela como principal. Verifique se ela não está minimizada. Erro: {e}")

    def get_screenshot(self):
        rect = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bottom = rect

        monitor = {
            "top": top,
            "left": left,
            "width": right - left,
            "height": bottom - top,
        }

        # A biblioteca mss retorna uma imagem com 4 canais (RGBA).
        # A linha abaixo garante que ela seja convertida para o tipo de dado uint8,
        # que é o formato esperado pelo OpenCV.
        img = np.array(self.sct.grab(monitor), dtype=np.uint8)
        return img[:, :, :3]

    @staticmethod
    def list_windows():
        """Lista todas as janelas visíveis e retorna uma lista de (hwnd, titulo)."""
        windows = []
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        
        win32gui.EnumWindows(callback, None)
        return windows