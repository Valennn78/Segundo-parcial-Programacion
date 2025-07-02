import pygame

# cargamos y dimensionamos cada parte del cuerpo
cabeza_img = pygame.transform.scale(pygame.image.load("imagenes/bocha.png"), (50, 50))
torso_img = pygame.transform.scale(pygame.image.load("imagenes/torso.png"), (60, 80))
brazo_izquierdo_img = pygame.transform.scale(pygame.image.load("imagenes/brazoizq.png"), (50, 90))
Brazo_derecho_img = pygame.transform.scale(pygame.image.load("imagenes/brazoder.png"), (50, 90))
pierna_izquierda_img = pygame.transform.scale(pygame.image.load("imagenes/piernaizq.png"), (65, 120))
pierna_derecha_img = pygame.transform.scale(pygame.image.load("imagenes/piernader.png"), (65, 120))
