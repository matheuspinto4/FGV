import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from utils import *


def create_page2(window, page1, page3):
    canvas = tk.Canvas(
    window,
    bg = "#ECECEC",
    height = 682,
    width = 1254,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    bt_go_to_page1 = tk.Button(master=window, text="Go to Page 1", command=lambda:go_to_page1(window, page1))
    bt_go_to_page1.place(x=16, y=143)

    bt_go_to_page3 = tk.Button(master=window, text="Go to Page 3", command=lambda:go_to_page3(window, page3))
    bt_go_to_page3.place(x=16, y=340)

    x = np.arange(100)
    y = np.random.rand(100)
    plot_line(x1=502, y1=300, x2=1227, y2=653, master=window, plot_values=(x, y))
    # window.after(100, lambda: update_page2(window))