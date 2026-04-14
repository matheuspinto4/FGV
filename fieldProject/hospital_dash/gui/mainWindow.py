from pathlib import Path

import tkinter as tk
from utils import *
from page1 import *
from page2 import *
from page3 import *

#  Criando a Window Principal do programa
window = tk.Tk()
window.geometry("1254x682")
window.configure(bg = "#ECECEC")


#  Inicializando os frames de cada página
page1 = tk.Frame(master=window, bg="#ECECEC")
page2 = tk.Frame(master=window, bg="#ECECEC")
page3 = tk.Frame(master=window, bg="#ECECEC")

#  Alocando a primeira página como inicial
page1.place(relwidth=1, relheight=1)


#  Preenchendo cada página com os seus conteúdos
create_page1(window=page1, page2=page2, page3=page3)
create_page2(window=page2, page1=page1, page3=page3)
create_page3(window=page3, page1=page1, page2=page2)

#  Configurando o Window Principal
window.resizable(False, False)
window.mainloop()
