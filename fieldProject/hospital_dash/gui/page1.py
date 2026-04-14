import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from utils import *


def create_page1(window, page2, page3):
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
    canvas.create_rectangle(
        1.0,
        0.0,
        69.0,
        680.0,
        fill="#005AA9",
        outline="")

    canvas.create_rectangle(
        2.0,
        572.0,
        64.0,
        634.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        16.0,
        246.0,
        49.0,
        279.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        16.0,
        151.0,
        50.0,
        185.0,
        fill="#FFFFFF",
        outline="")
    bt_go_to_page2 = tk.Button(master=window, text="Go to Page 2", command=lambda:go_to_page2(window, page2))
    bt_go_to_page2.place(x=16, y=246)

    canvas.create_rectangle(
        16.0,
        340.0,
        50.0,
        373.0,
        fill="#FFFFFF",
        outline="")
    bt_go_to_page3 = tk.Button(master=window, text="Go to Page 3", command=lambda:go_to_page3(window, page3))
    bt_go_to_page3.place(x=16, y=340)

    canvas.create_rectangle(
        79.0,
        17.0,
        1241.0,
        79.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        122.0,
        37.0,
        anchor="nw",
        text="Painel de acompanhamento da Fila Hospitalar",
        fill="#005AA9",
        font=("WorkSans Bold", 14 )
    )

    canvas.create_rectangle(
        606.0,
        29.0,
        606.0,
        66.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        940.0,
        35.0,
        1117.0,
        62.0,
        fill="#ECECEC",
        outline="")

    canvas.create_text(
        959.0,
        39.0,
        anchor="nw",
        text="Selecionar dia",
        fill="#000000",
        font=("Comic San MS", 12)
    )

    canvas.create_text(
        1087.0,
        39.0,
        anchor="nw",
        text=">",
        fill="#000000",
        font=("Comic San MS", 13 )
    )

    canvas.create_rectangle(
        80.0,
        234.0,
        272.0,
        371.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        104.0,
        245.0,
        243.0,
        263.0,
        fill="#DC3545",
        outline="")

    canvas.create_rectangle(
        104.0,
        245.0,
        243.0,
        263.0,
        fill="#DC3545",
        outline="")

    canvas.create_rectangle(
        104.0,
        245.0,
        243.0,
        263.0,
        fill="#DC3545",
        outline="")

    canvas.create_rectangle(
        80.0,
        382.0,
        272.0,
        518.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        80.0,
        529.0,
        475.0,
        663.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        285.0,
        234.0,
        476.0,
        371.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        309.0,
        245.0,
        450.0,
        263.0,
        fill="#DC3545",
        outline="")

    canvas.create_rectangle(
        283.0,
        382.0,
        475.0,
        518.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        283.0,
        382.0,
        475.0,
        518.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        92.0,
        388.0,
        256.0,
        406.0,
        fill="#E0CE05",
        outline="")

    canvas.create_rectangle(
        297.0,
        388.0,
        462.0,
        406.0,
        fill="#E0CE05",
        outline="")

    canvas.create_rectangle(
        200.0,
        541.0,
        353.0,
        561.0,
        fill="#02A98A",
        outline="")

    canvas.create_text(
        137.0,
        246.0,
        anchor="nw",
        text="Previsão UTI",
        fill="#FFFFFF",
        font=("Sen Bold", 10 )
    )

    canvas.create_text(
        339.0,
        246.0,
        anchor="nw",
        text="Capacidade UTI",
        fill="#FFFFFF",
        font=("Sen Bold", 10 )
    )

    canvas.create_text(
        164.0,
        292.0,
        anchor="nw",
        text="4",
        fill="#000000",
        font=("Comic San MS", 24 )
    )

    canvas.create_text(
        359.0,
        292.0,
        anchor="nw",
        text="10",
        fill="#000000",
        font=("Comic San MS", 24 )
    )

    canvas.create_text(
        366.0,
        441.0,
        anchor="nw",
        text="20",
        fill="#000000",
        font=("Comic San MS", 24 )
    )

    canvas.create_text(
        164.0,
        441.0,
        anchor="nw",
        text=8,
        fill="#000000",
        font=("Comic San MS", 30 )
    )

    canvas.create_text(
        255.0,
        582.0,
        anchor="nw",
        text="18",
        fill="#000000",
        font=("Comic San MS", 24 )
    )

    canvas.create_text(
        116.0,
        389.0,
        anchor="nw",
        text="Previsão Internação ",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_text(
        316.0,
        389.0,
        anchor="nw",
        text="Capacidade Internação ",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_text(
        237.0,
        542.0,
        anchor="nw",
        text="Previsão Alta",
        fill="#FFFFFF",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        79.0,
        88.0,
        475.0,
        224.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        200.0,
        103.0,
        350.0,
        124.0,
        fill="#ECECEC",
        outline="")

    canvas.create_text(
        261.0,
        142.0,
        anchor="nw",
        text="30",
        fill="#000000",
        font=("Comic San MS", 24 )
    )

    canvas.create_text(
        224.0,
        105.0,
        anchor="nw",
        text="Total de Pacientes",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        486.0,
        88.0,
        856.0,
        224.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        600.0,
        161.0,
        763.0,
        178.0,
        fill="#E0CE05",
        outline="")

    canvas.create_rectangle(
        600.0,
        182.0,
        763.0,
        201.0,
        fill="#02A98A",
        outline="")

    canvas.create_text(
        654.0,
        161.0,
        anchor="nw",
        text="Internação ",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_text(
        671.0,
        183.0,
        anchor="nw",
        text="Alta",
        fill="#FFFFFF",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        602.0,
        103.0,
        756.0,
        121.0,
        fill="#ECECEC",
        outline="")

    canvas.create_text(
        650.0,
        103.0,
        anchor="nw",
        text="Categorias",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        870.0,
        87.0,
        1240.0,
        223.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        998.0,
        102.0,
        1152.0,
        120.0,
        fill="#ECECEC",
        outline="")

    canvas.create_text(
        1043.0,
        102.0,
        anchor="nw",
        text="Categorias",
        fill="#000000",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        600.0,
        139.0,
        763.0,
        156.0,
        fill="#DC3545",
        outline="")

    canvas.create_text(
        672.0,
        139.0,
        anchor="nw",
        text="UTI",
        fill="#FFFFFF",
        font=("Sen Bold", 10 )
    )

    canvas.create_rectangle(
        920.0,
        140.0,
        1033.0,
        198.0,
        fill="#005AA9",
        outline="")

    canvas.create_rectangle(
        1094.0,
        140.0,
        1206.0,
        198.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        945.0,
        159.0,
        anchor="nw",
        text="Por Hora",
        fill="#FFFFFF",
        font=("Sen Bold", 12 )
    )

    canvas.create_text(
        1118.0,
        159.0,
        anchor="nw",
        text="Por Turno",
        fill="#000000",
        font=("Sen Bold", 12 )
    )

    canvas.create_rectangle(
        489.0,
        234.0,
        1241.0,
        665.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        568.0,
        257.0,
        1183.0,
        279.0,
        fill="#ECECEC",
        outline="")

    canvas.create_text(
        790.0,
        259.0,
        anchor="nw",
        text="Volume da Fila Hospitalar",
        fill="#000000",
        font=("Sen Bold", 12 )
    )

    canvas.create_rectangle(
        502.0,
        300.0,
        1227.0,
        653.0,
        fill="#D9D9D9",
        outline="")
    
    update_page1(window=window)



def update_page1(window):
    x = np.arange(100)
    y = np.random.rand(100)
    plot_line(x1=502, y1=300, x2=1227, y2=653, master=window, plot_values=(x, y))
    window.after(100, lambda: update_page1(window))

