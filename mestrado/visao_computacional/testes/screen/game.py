import pygame 
import numpy as np
import cv2


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

pygame.init()

def read_img(img_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    scale_factor = min(SCREEN_HEIGHT / h, SCREEN_WIDTH / (2*w))
    img = cv2.resize(img, dsize=None, fx=scale_factor, fy=scale_factor)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.transpose(img, (1, 0, 2))  
    return img

img = read_img('2.png')

screen_height = min(img.shape[1], SCREEN_HEIGHT)
screen_width = min(img.shape[0], SCREEN_WIDTH)
display = pygame.display.set_mode((2*screen_width, screen_height + 100))

img2 = img
surf_original = pygame.surfarray.make_surface(img)
surf_modified = pygame.surfarray.make_surface(img2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.blit(surf_original, (0, 0))
    display.blit(surf_modified, (screen_width, 0))
    
    pygame.display.update()

pygame.quit()
