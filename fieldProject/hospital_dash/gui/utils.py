import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def go_to_page1(currentPage, page1):
    currentPage.place_forget()
    page1.place(relheight=1, relwidth=1)


def go_to_page2(currentPage, page2):
    currentPage.place_forget()
    page2.place(relheight=1, relwidth=1)


def go_to_page3(currentPage, page3):
    currentPage.place_forget()
    page3.place(relheight=1, relwidth=1)


def plot_line(x1, y1, x2, y2, master, plot_values, back_color="#FFFFFF"):
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches

    fig_1 = plt.Figure(figsize=((x2 - x1)*px, (y2 - y1)*px ), facecolor=back_color)
    ax_1 = fig_1.add_subplot()
    ax_1.plot(*plot_values)
    ax_1.spines['top'].set_color(back_color)
    ax_1.spines['right'].set_color(back_color)

    fig_1.tight_layout(pad=0)

    canvas1 = FigureCanvasTkAgg(figure=fig_1, master=master)
    canvas1.draw()
    canvas1.get_tk_widget().place(x=x1, y=y1)
