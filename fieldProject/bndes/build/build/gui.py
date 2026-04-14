import customtkinter as ctk
import ctypes

# Corrige o DPI para telas de alta resolução (Windows)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Configuração inicial da janela
ctk.set_appearance_mode("light")  # ou "dark"
ctk.set_default_color_theme("blue")  # pode trocar por "green", "dark-blue", etc.

window = ctk.CTk()
window.geometry('588x342')
window.title("Exemplo CustomTkinter")

# Canvas (usando CTkCanvas do tkinter padrão, pois CustomTkinter não tem o seu próprio)
canvas = ctk.CTkCanvas(
    window,
    bg="#FFFFFF",
    height=342,
    width=588,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Campo de entrada (Entry)
e1 = ctk.CTkEntry(
    master=window,
    placeholder_text="Digite algo...",
    width=388 - 66, height=156 - 68
)
e1.place(x=66, y=68)

# Retângulo cinza
canvas.create_rectangle(
    66.0,
    246.0,
    536.0,
    314.0,
    fill="#D9D9D9",
    outline=""
)

# Botão
bt = ctk.CTkButton(
    master=window,
    text="OK",
    command=lambda: print(e1.get()),
    width=489 - 428, height=150 - 74
)
bt.place(x=428, y=74)

window.mainloop()
