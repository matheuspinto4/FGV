import cv2
import time
import numpy as np
from window_capture import WindowCapture

# O nome da janela do seu jogo
WINDOW_NAME = "Vampire Survivors"
step=10
# --- Configuração inicial dos pontos de origem ---
# Estes são apenas valores de exemplo. Você irá ajustá-los em tempo real.
pts_src = np.array([
    [0, 0],  # Ponto 0 (topo-esquerdo)
    [960, 0],  # Ponto 1 (topo-direito)
    [960, 1080],  # Ponto 2 (baixo-direito)
    [0, 1080]   # Ponto 3 (baixo-esquerdo)
], dtype=np.float32)

# Configuração dos pontos de destino (mantém-se a mesma)
width = 960
height = 1080
pts_dst = np.array([
    [0, 0],
    [width - 1, 0],
    [width - 1, height - 1],
    [0, height - 1]
], dtype=np.float32)

# Variável de estado para controlar qual ponto está selecionado
current_point_index = 0

try:
    window_list = WindowCapture.list_windows()
    if not window_list:
        raise Exception("Nenhuma janela visível encontrada.")

    print("Janelas disponíveis para captura:")
    for i, (hwnd, title) in enumerate(window_list):
        print(f"[{i}] {title}")
    
    choice = int(input("Digite o número da janela que deseja capturar: "))
    selected_hwnd = window_list[choice][0]

    wincap = WindowCapture(selected_hwnd)
except Exception as e:
    print(f"Erro de inicialização: {e}")
    exit()

# Inicializa o temporizador para calcular o FPS
loop_time = time.time()

while True:
    # Captura a tela do jogo e garante o formato correto
    screenshot = wincap.get_screenshot()
    screenshot = np.ascontiguousarray(screenshot, dtype=np.uint8)

    # --- Lógica de controle de teclado para ajustar a projeção ---
    key = cv2.waitKey(1)
    
    # Tecla 'F' para alternar entre os pontos
    if key == ord('f'):
        current_point_index = (current_point_index + 1) % 4
        print(f"Ponto selecionado: {current_point_index}")

    # Teclas W, S, A, D para mover o ponto selecionado
    if key == ord('w'):
        pts_dst[current_point_index][1] -= step  # Move para cima
    if key == ord('s'):
        pts_dst[current_point_index][1] += step  # Move para baixo
    if key == ord('a'):
        pts_dst[current_point_index][0] -= step  # Move para a esquerda
    if key == ord('d'):
        pts_dst[current_point_index][0] += step  # Move para a direita

    # Recalcula a matriz de projeção a cada frame, pois os pontos podem ter mudado
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    # Aplica a matriz de projeção ao screenshot
    result = cv2.warpPerspective(screenshot, matrix, (width, height))

    # --- Visualização ---
    # Desenha todos os pontos, e o ponto selecionado é destacado em verde
    for i, point in enumerate(pts_src):
        color = (0, 0, 255)  # Vermelho para pontos não selecionados
        radius = 5
        if i == current_point_index:
            color = (0, 255, 0)  # Verde para o ponto selecionado
            radius = 8
        cv2.circle(screenshot, (int(point[0]), int(point[1])), radius, color, -1)
    
    # Exibe a numeração do ponto selecionado na tela
    cv2.putText(screenshot, f"Ponto: {current_point_index}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Original", screenshot)
    cv2.imshow("Vista Achatada (Perspectiva)", result)

    # Pressione 'q' para sair
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    
    # Calcula e exibe o FPS
    fps = 1 / (time.time() - loop_time)
    print(f"FPS: {fps:.2f} | Ponto {current_point_index}: {pts_dst[current_point_index]}")
    loop_time = time.time()