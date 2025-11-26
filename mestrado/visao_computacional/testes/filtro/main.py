import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, Frame, Label, Button, Scale, HORIZONTAL, BOTH, SUNKEN, X, LEFT, RAISED, messagebox, Checkbutton, Scrollbar, Canvas
from PIL import Image, ImageTk

# --- Funções de Visão Computacional de Apoio ---

def numpy_to_phototk(img_array, max_width=450):
    """
    Converte um array NumPy (float32, [0, 1], grayscale ou BGR) para PhotoImage.
    Redimensiona para caber na tela mantendo a proporção.
    Retorna (PhotoImage, largura, altura).
    """
    try:
        # 1. Converter para 8-bit (0-255)
        img_8bit = np.clip(img_array * 255.0, 0, 255).astype(np.uint8)

        # 2. Se for grayscale (2D), converter para 3 canais BGR
        if img_8bit.ndim == 2:
            img_8bit = cv2.cvtColor(img_8bit, cv2.COLOR_GRAY2BGR)

        # 3. Converter BGR (OpenCV default) para RGB (PIL/Tkinter default).
        if img_8bit.ndim == 3:
            # Trocar canais BGR (0, 1, 2) para RGB (2, 1, 0)
            img_rgb = img_8bit[:, :, ::-1]
        else:
            img_rgb = img_8bit


        # 4. Criar imagem PIL
        img_pil = Image.fromarray(img_rgb)
        
        # 5. Redimensionar para caber na tela mantendo proporção
        if img_pil.width > max_width:
            ratio = max_width / img_pil.width
            new_height = int(img_pil.height * ratio)
            # Resampling.LANCZOS para redimensionamento de alta qualidade
            img_pil = img_pil.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # 6. Criar PhotoImage do Tkinter
        tk_img = ImageTk.PhotoImage(img_pil)
        return tk_img, img_pil.width, img_pil.height

    except Exception as e:
        print(f"Erro na conversão NumPy para PhotoImage: {e}")
        return None, 0, 0

def gaussian_vector_1d(kernel_size, sigma):
    """Gera um vetor 1D gaussiano normalizado para filtro separável."""
    kernel_size = int(kernel_size)
    kernel_size = max(3, kernel_size if kernel_size % 2 != 0 else kernel_size + 1)
    sigma = max(0.01, sigma)
    
    half_size = kernel_size // 2
    x = np.arange(-half_size, half_size + 1).astype(np.float32)
    g = np.exp(-(x**2) / (2 * sigma**2))
    g = g / g.sum()
    
    return g.reshape(1, -1).astype(np.float32)

def apply_gaussian_blur(img, kernel_size, sigma):
    """
    Aplica o filtro de desfoque Gaussiano. Pode ser usado como pre-processamento.
    Funciona em canais BGR ou Grayscale.
    """
    ksize = int(kernel_size)
    ksize = max(3, ksize if ksize % 2 != 0 else ksize + 1)
    sigma = float(sigma)
    
    # Se sigma=0, OpenCV calcula sigma com base no tamanho do kernel
    return cv2.GaussianBlur(img, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)

def apply_dog_filter(img, kernel_size, sigma, k, t, e, phi, color_mode):
    """
    Aplica o filtro Difference of Gaussians (DoG/XDoG).
    Retorna uma imagem float32 [0, 1] em grayscale ou BGR.
    """
    sigma1 = max(0.01, float(sigma))
    k = max(1.01, float(k)) 
    kernel_size = int(kernel_size)
    
    g5_1_1d = gaussian_vector_1d(kernel_size=kernel_size, sigma=sigma1)
    g5_2_1d = gaussian_vector_1d(kernel_size=kernel_size, sigma=sigma1 * k)
    
    kernel_2d_1 = g5_1_1d.T.dot(g5_1_1d)
    kernel_2d_2 = g5_2_1d.T.dot(g5_2_1d)
    
    
    if color_mode:
        # Processamento em Cores (separado por canal BGR)
        channels = cv2.split(img)
        processed_channels = []
        
        for channel in channels:
            img1 = cv2.filter2D(channel, -1, kernel_2d_1, borderType=cv2.BORDER_REPLICATE)
            img2 = cv2.filter2D(channel, -1, kernel_2d_2, borderType=cv2.BORDER_REPLICATE)
            diff = (1.0 + t) * img1 - t * img2
            processed_channels.append(diff)
            
        diff_merged = cv2.merge(processed_channels) 
        diff_clipped = np.clip(diff_merged, 0.0, 1.0)
        diff_enhanced = np.where(diff_clipped > e, 1.0, 1.0 + np.tanh(phi * (diff_clipped - e)))
        final_img = 1.0 - diff_enhanced
        
    else: 
        # Processamento em Grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        img1 = cv2.filter2D(gray_img, -1, kernel_2d_1, borderType=cv2.BORDER_REPLICATE)
        img2 = cv2.filter2D(gray_img, -1, kernel_2d_2, borderType=cv2.BORDER_REPLICATE)
        
        diff = (1.0 + t) * img1 - t * img2
        diff_clipped = np.clip(diff, 0.0, 1.0)
        diff_enhanced = np.where(diff_clipped > e, 1.0, 1.0 + np.tanh(phi * (diff_clipped - e)))
        final_img = 1.0 - diff_enhanced
        
    return final_img

def apply_canny_filter(img, low_threshold, high_threshold):
    """
    Aplica o Canny Edge Detector. 
    O Canny só funciona em imagens Grayscale.
    Retorna uma imagem float32 [0, 1] em grayscale.
    """
    # 1. Converte para Grayscale
    gray_img_8bit = np.clip(img * 255.0, 0, 255).astype(np.uint8)
    gray_img = cv2.cvtColor(gray_img_8bit, cv2.COLOR_BGR2GRAY)
    
    # 2. Aplica o Canny
    edges = cv2.Canny(gray_img, low_threshold, high_threshold)
    
    # 3. Normaliza para [0, 1] float32 para manter o pipeline
    return edges.astype(np.float32) / 255.0

def apply_sobel_filter(img, ksize, scale):
    """
    Aplica o Sobel Edge Detector. 
    Retorna o magnitude do gradiente (Grayscale float32 [0, 1]).
    """
    ksize = int(ksize)
    # ksize deve ser ímpar, de 1 a 31
    ksize = max(3, ksize if ksize % 2 != 0 else ksize + 1)
    scale = float(scale)
    
    # 1. Converter para Grayscale e 8-bit
    if img.ndim == 3:
        gray_img_8bit = cv2.cvtColor(np.clip(img * 255.0, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    else: # Já é 2D/Grayscale
        gray_img_8bit = np.clip(img * 255.0, 0, 255).astype(np.uint8)

    # 2. Calcular gradientes X e Y (usando cv2.CV_64F para evitar estouro de precisão)
    grad_x = cv2.Sobel(gray_img_8bit, cv2.CV_64F, 1, 0, ksize=ksize, scale=scale)
    grad_y = cv2.Sobel(gray_img_8bit, cv2.CV_64F, 0, 1, ksize=ksize, scale=scale)

    # 3. Calcular a magnitude do gradiente (aproximada, soma ponderada dos absolutos)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    sobel_combined_8bit = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    # 4. Normalizar para [0, 1] float32 para manter o pipeline
    return sobel_combined_8bit.astype(np.float32) / 255.0


# --- Classe Principal da Aplicação Tkinter ---

class DogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Filtro de Visão Computacional (DoG, Canny, Sobel, Blur)")
        self.root.geometry("1100x700") 
        
        # Variáveis de estado da imagem
        self.original_img_bgr = None 
        self.original_tk_img = None
        self.processed_tk_img = None
        
        # Variáveis de Seleção de Filtro
        self.dog_selected_var = tk.BooleanVar(value=True)
        self.canny_selected_var = tk.BooleanVar(value=False)
        self.sobel_selected_var = tk.BooleanVar(value=False) # NOVO
        self.blur_selected_var = tk.BooleanVar(value=False)  # NOVO
        self.color_mode_var = tk.BooleanVar(value=False) 
        
        # Variáveis de Parâmetros DoG
        self.kernel_size_var = tk.IntVar(value=5)
        self.sigma_var = tk.DoubleVar(value=0.25)
        self.k_var = tk.DoubleVar(value=10.0) 
        self.t_var = tk.DoubleVar(value=0.1) 
        self.e_var = tk.DoubleVar(value=0.9) 
        self.phi_var = tk.DoubleVar(value=3.0) 

        # Variáveis de Parâmetros Canny
        self.canny_low_var = tk.IntVar(value=50)
        self.canny_high_var = tk.IntVar(value=150)
        
        # Variáveis de Parâmetros Sobel (NOVO)
        self.sobel_ksize_var = tk.IntVar(value=3)
        self.sobel_scale_var = tk.DoubleVar(value=1.0)
        
        # Variáveis de Parâmetros Gaussian Blur (NOVO)
        self.blur_ksize_var = tk.IntVar(value=5)
        self.blur_sigma_var = tk.DoubleVar(value=1.5)
        
        # UI Setup
        self.build_ui()
        self.display_placeholder()
        
    def build_ui(self):
        """Constrói a interface de usuário com controles e visualizadores, incluindo a rolagem."""
        
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)

        # 1. Frame Container (Holds Canvas and Scrollbar)
        control_container = Frame(main_frame, width=320, relief=RAISED, borderwidth=2, padx=5, pady=5, bg='#f0f0f0')
        control_container.pack(side=LEFT, fill="y", padx=10, pady=10)

        # 1.1. Setup Scrollbar and Canvas
        canvas = tk.Canvas(control_container, bg='#f0f0f0', highlightthickness=0)
        
        scrollbar = tk.Scrollbar(control_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 1.2. Inner Frame (O conteúdo real que irá rolar)
        self.control_frame_inner = Frame(canvas, bg='#f0f0f0', padx=5, pady=5)
        canvas_window = canvas.create_window((0, 0), window=self.control_frame_inner, anchor="nw")

        # Configurações de rolagem:
        self.control_frame_inner.bind("<Configure>", 
                                  lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # --- CONTEÚDO NO FRAME INTERNO (SCROLLABLE) ---

        Label(self.control_frame_inner, text="Controles do Processamento", font=("Inter", 16, "bold"), pady=5, bg='#f0f0f0').pack(fill=X)
        
        # Botão Carregar Imagem
        Button(self.control_frame_inner, text="1. Carregar Imagem", command=self.load_image, bg="#2196F3", fg="white", 
               font=("Inter", 12, "bold"), pady=8, relief=RAISED).pack(fill=X, pady=(15, 10))
        
        # --- SELEÇÃO DE FILTROS ---
        filter_select_frame = Frame(self.control_frame_inner, bg='#e9e9e9', relief=SUNKEN, borderwidth=1, padx=5, pady=5)
        filter_select_frame.pack(fill=X, pady=10)
        Label(filter_select_frame, text="Selecione os Filtros (Ordem: Blur -> DoG -> Canny -> Sobel)", font=("Inter", 10, "bold"), bg='#e9e9e9').pack(anchor='w', pady=5)
        
        # Checkbox Gaussian Blur (NOVO)
        Checkbutton(filter_select_frame, text="Gaussian Blur (Suavização)", variable=self.blur_selected_var, command=self.update_dog_image, font=("Inter", 10), bg='#e9e9e9', activebackground='#e9e9e9', selectcolor='#ffffff').pack(anchor='w', padx=5)
        # Checkbox DoG
        Checkbutton(filter_select_frame, text="Difference of Gaussians (DoG)", variable=self.dog_selected_var, command=self.update_dog_image, font=("Inter", 10), bg='#e9e9e9', activebackground='#e9e9e9', selectcolor='#ffffff').pack(anchor='w', padx=5)
        # Checkbox Canny
        Checkbutton(filter_select_frame, text="Canny Edge Detector", variable=self.canny_selected_var, command=self.update_dog_image, font=("Inter", 10), bg='#e9e9e9', activebackground='#e9e9e9', selectcolor='#ffffff').pack(anchor='w', padx=5)
        # Checkbox Sobel (NOVO)
        Checkbutton(filter_select_frame, text="Sobel Edge Detector", variable=self.sobel_selected_var, command=self.update_dog_image, font=("Inter", 10), bg='#e9e9e9', activebackground='#e9e9e9', selectcolor='#ffffff').pack(anchor='w', padx=5)
        
        # Checkbox Modo de Cor
        Checkbutton(filter_select_frame, text="Modo Cores (Apenas DoG/XDoG)", variable=self.color_mode_var, command=self.update_dog_image, font=("Inter", 10, "bold"), bg='#e9e9e9', activebackground='#e9e9e9', selectcolor='#ffffff').pack(anchor='w', padx=5, pady=(5,0))

        # --- PARÂMETROS DO FILTRO ---

        # Função auxiliar para criar sliders
        def create_slider(parent, text, variable, from_, to, resolution, color):
            frame = Frame(parent, bg='#f0f0f0')
            frame.pack(fill=X, pady=2)
            
            Label(frame, text=f"{text}:", width=12, anchor='w', font=("Inter", 10), bg='#f0f0f0', fg=color).pack(side=LEFT)
            
            slider = Scale(frame, from_=from_, to=to, resolution=resolution, orient=HORIZONTAL, 
                           variable=variable, command=self.update_dog_image, length=180, showvalue=True,
                           troughcolor="#BDBDBD", activebackground=color)
            slider.pack(side=LEFT, expand=True, fill=X)
            return slider

        # Gaussian Blur Parameters Section (NOVO)
        Label(self.control_frame_inner, text="Parâmetros Gaussian Blur", font=("Inter", 12, "bold"), bg='#f0f0f0', fg='#9C27B0').pack(fill=X, pady=(15, 0)) # Roxa
        create_slider(self.control_frame_inner, "Kernel Size (ímpar)", self.blur_ksize_var, 3, 31, 2, '#9C27B0')
        create_slider(self.control_frame_inner, "Sigma ($\sigma$)", self.blur_sigma_var, 0.0, 5.0, 0.1, '#9C27B0')

        # DoG Parameters Section
        Label(self.control_frame_inner, text="Parâmetros DoG", font=("Inter", 12, "bold"), bg='#f0f0f0', fg='#4CAF50').pack(fill=X, pady=(10, 0)) # Verde
        create_slider(self.control_frame_inner, "Kernel Size (ímpar)", self.kernel_size_var, 3, 21, 2, '#4CAF50')
        create_slider(self.control_frame_inner, "Sigma 1 ($\sigma$)", self.sigma_var, 0.1, 5.0, 0.05, '#4CAF50')
        create_slider(self.control_frame_inner, "Sigma Ratio ($k$)", self.k_var, 1.01, 20.0, 0.1, '#4CAF50')
        create_slider(self.control_frame_inner, "Diff Boost ($t$)", self.t_var, 0.0, 100.0, 0.5, '#4CAF50')
        create_slider(self.control_frame_inner, "Threshold ($e$)", self.e_var, 0.0, 1.0, 0.01, '#4CAF50')
        create_slider(self.control_frame_inner, "Tanh Gain ($\phi$)", self.phi_var, 0.1, 50.0, 0.5, '#4CAF50')
        
        # Canny Parameters Section
        Label(self.control_frame_inner, text="Parâmetros Canny", font=("Inter", 12, "bold"), bg='#f0f0f0', fg='#00BCD4').pack(fill=X, pady=(15, 0)) # Ciano
        create_slider(self.control_frame_inner, "Threshold Inferior", self.canny_low_var, 0, 255, 1, '#00BCD4')
        create_slider(self.control_frame_inner, "Threshold Superior", self.canny_high_var, 0, 255, 1, '#00BCD4')
        
        # Sobel Parameters Section (NOVO)
        Label(self.control_frame_inner, text="Parâmetros Sobel", font=("Inter", 12, "bold"), bg='#f0f0f0', fg='#FF5722').pack(fill=X, pady=(15, 0)) # Laranja
        create_slider(self.control_frame_inner, "Kernel Size (ímpar)", self.sobel_ksize_var, 3, 31, 2, '#FF5722')
        create_slider(self.control_frame_inner, "Scale (Escala)", self.sobel_scale_var, 0.1, 5.0, 0.1, '#FF5722')
        

        # Botão Aplicar Pipeline
        Button(self.control_frame_inner, text="2. Aplicar Pipeline de Filtros", command=self.update_dog_image, bg="#FF9800", fg="white", 
               font=("Inter", 12, "bold"), pady=8, relief=RAISED).pack(fill=X, pady=(25, 10))


        # 2. Frame de Visualização (Direita)
        view_frame = Frame(main_frame)
        view_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # 2.1. Visualizador Original
        original_frame = Frame(view_frame, relief=SUNKEN, borderwidth=1)
        original_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        Label(original_frame, text="Imagem Original", font=("Inter", 12, "bold")).pack(fill=X, pady=5)
        
        self.canvas_original = Label(original_frame, bg="#E0E0E0", width=450, height=450, relief=SUNKEN)
        self.canvas_original.pack(fill=BOTH, expand=True)

        # 2.2. Visualizador Processado
        processed_frame = Frame(view_frame, relief=SUNKEN, borderwidth=1)
        processed_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        Label(processed_frame, text="Imagem Processada", font=("Inter", 12, "bold")).pack(fill=X, pady=5)
        
        self.canvas_processed = Label(processed_frame, bg="#E0E0E0", width=450, height=450, relief=SUNKEN)
        self.canvas_processed.pack(fill=BOTH, expand=True)

    def display_placeholder(self):
        """Exibe um placeholder nos Labels de imagem."""
        placeholder_text = "Carregue uma imagem para começar (JPG, PNG)"
        
        try:
            img = Image.new('RGB', (450, 450), color='#E0E0E0')
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default() 
            
            text_bbox = draw.textbbox((0, 0), placeholder_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (450 - text_width) / 2
            y = (450 - text_height) / 2
            draw.text((x, y), placeholder_text, fill='black', font=font)
            
            self.original_tk_img = ImageTk.PhotoImage(img)
            self.processed_tk_img = ImageTk.PhotoImage(img)
            
            self.canvas_original.config(image=self.original_tk_img, width=450, height=450, text="")
            self.canvas_processed.config(image=self.processed_tk_img, width=450, height=450, text="")
            self.canvas_original.image = self.original_tk_img 
            self.canvas_processed.image = self.processed_tk_img
        except Exception:
            self.canvas_original.config(text=placeholder_text)
            self.canvas_processed.config(text=placeholder_text)


    def load_image(self):
        """Abre uma caixa de diálogo para carregar uma imagem e a exibe."""
        f_types = [('Imagens', '*.jpg;*.png;*.jpeg')]
        path = filedialog.askopenfilename(filetypes=f_types, title="Selecione uma Imagem")
        
        if not path:
            return
            
        try:
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Erro de Leitura", "Não foi possível carregar a imagem. Verifique o caminho ou formato.")
                return

            self.original_img_bgr = img.astype(np.float32) / 255.0
            
            tk_img, w, h = numpy_to_phototk(self.original_img_bgr)
            
            if tk_img:
                self.original_tk_img = tk_img
                self.canvas_original.config(image=self.original_tk_img, width=w, height=h, text="")
                self.canvas_original.image = self.original_tk_img

                self.update_dog_image()

        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro ao carregar ou processar a imagem: {e}")
            self.original_img_bgr = None
            self.display_placeholder()
            
    def process_image_pipeline(self, img_bgr):
        """Aplica os filtros selecionados sequencialmente."""
        current_img = img_bgr
        
        # 1. Obter parâmetros
        params = {
            'dog': {
                'kernel_size': self.kernel_size_var.get(), 'sigma': self.sigma_var.get(), 'k': self.k_var.get(),
                't': self.t_var.get(), 'e': self.e_var.get(), 'phi': self.phi_var.get(), 
                'color_mode': self.color_mode_var.get()
            },
            'canny': {
                'low_t': self.canny_low_var.get(), 'high_t': self.canny_high_var.get()
            },
            'sobel': {
                'ksize': self.sobel_ksize_var.get(), 'scale': self.sobel_scale_var.get()
            },
            'blur': {
                'ksize': self.blur_ksize_var.get(), 'sigma': self.blur_sigma_var.get()
            }
        }
        
        # --- Ordem de Aplicação dos Filtros ---
        
        # 2. Aplicar Gaussian Blur (Primeiro passo para suavizar antes de detecção de bordas)
        if self.blur_selected_var.get():
            current_img = apply_gaussian_blur(
                current_img, params['blur']['ksize'], params['blur']['sigma']
            )

        # 3. Aplicar DoG/XDoG
        if self.dog_selected_var.get():
            current_img = apply_dog_filter(
                current_img, **params['dog']
            )

        # 4. Aplicar Canny
        if self.canny_selected_var.get():
            # Canny requer BGR (ou Grayscale 2D) de entrada. Se for Grayscale (2D), convertemos para BGR temporariamente.
            if current_img.ndim == 2:
                # Converte Grayscale [0, 1] para BGR [0, 1] antes de passar para Canny
                current_img_3ch = cv2.cvtColor(np.clip(current_img * 255.0, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0
            else:
                current_img_3ch = current_img

            current_img = apply_canny_filter(
                current_img_3ch, params['canny']['low_t'], params['canny']['high_t']
            )
            # Saída Canny é sempre Grayscale (2D float32)
        
        # 5. Aplicar Sobel (Último, pois é outro detector de bordas)
        if self.sobel_selected_var.get():
            current_img = apply_sobel_filter(
                current_img, **params['sobel']
            )
            # Saída Sobel é sempre Grayscale (2D float32)

        # Se nenhum filtro foi selecionado, retorna a imagem original.
        if not self.dog_selected_var.get() and not self.canny_selected_var.get() and not self.sobel_selected_var.get() and not self.blur_selected_var.get():
             return img_bgr # Retorna a imagem BGR original
             
        return current_img


    def update_dog_image(self, event=None):
        """Lê os parâmetros e executa o pipeline de filtros."""
        if self.original_img_bgr is None:
            return

        try:
            # Executa a sequência de filtros
            processed_img = self.process_image_pipeline(self.original_img_bgr)
            
            if processed_img is None:
                return

            # Exibir a imagem processada
            tk_img, w, h = numpy_to_phototk(processed_img)
            
            if tk_img:
                self.processed_tk_img = tk_img
                self.canvas_processed.config(image=self.processed_tk_img, width=w, height=h, text="")
                self.canvas_processed.image = self.processed_tk_img
                
        except Exception as err:
            print(f"Erro ao atualizar a imagem: {err}")
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro no pipeline de filtros: {err}")

    def run(self):
        """Inicia o loop principal do Tkinter."""
        self.root.mainloop()

# --- Bloco de Execução ---

if __name__ == '__main__':
    try:
        pass
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Certifique-se de que numpy, opencv-python (cv2) e Pillow (PIL) estão instalados:")
        print("pip install numpy opencv-python pillow")
        exit() 
    
    root = tk.Tk()
    app = DogApp(root)
    app.run()
