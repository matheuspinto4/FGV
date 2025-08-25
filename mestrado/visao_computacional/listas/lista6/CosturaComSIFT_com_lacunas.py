#%%
import cv2 as cv2
import numpy as np

#%% Carregar as imagens
imagem1 = cv2.imread('..\\Imagens\\keble_a.jpg')
imagem2 = cv2.imread('..\\Imagens\\keble_b.jpg')

cv2.imshow('Imagem1', imagem1)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%% Converter para escala de cinza
cinza1 = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
cinza2 = cv2.cvtColor(imagem2, cv2.COLOR_BGR2GRAY)

# Inicializar o detector SIFT e encontrar os pontos de interesse e descritores
sift = #objeto SIFT
pontos1, descritores1 = #detectar e computar os pontos de interesse e descritores (imagem1)
pontos2, descritores2 = #detectar e computar os pontos de interesse e descritores (imagem2)
#%%
imagem_com_circulos = cv2.drawKeypoints(imagem1, pontos1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Exibir a imagem com os círculos envolvendo as features
cv2.imshow('SIFT Features', imagem_com_circulos)
cv2.waitKey(0)
cv2.destroyAllWindows()
#%% Correspondência dos pontos de interesse
index_params = dict(algorithm=0, trees=5)
search_params = dict()
# Inicializar o matcher de features
matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
correspondencias = matcher.match(descritores1, descritores2)
correspondencias = sorted(correspondencias, key=lambda x: x.distance)

pontos1 = np.float32([pontos1[m.queryIdx].pt for m in correspondencias]).reshape(-1, 1, 2)
pontos2 = np.float32([pontos2[m.trainIdx].pt for m in correspondencias]).reshape(-1, 1, 2)

matriz_homografia, _ = cv2.findHomography(pontos2, pontos1, cv2.RANSAC, 5.0)

#%% Unir as imagens usando a matriz de homografia
imagem_unida = #usar a função warpPerspective para transformar uma das imagens
# unir as imagens (imagem1 e imagem_unida)

# Exibir o resultado
cv2.imshow("Imagem Costurada", imagem_unida)
cv2.waitKey(0)
cv2.destroyAllWindows()