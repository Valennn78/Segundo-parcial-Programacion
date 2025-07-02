
import pygame
from constantes import *

def crear_personaje():
    imagen = pygame.transform.scale(pygame.image.load("imagenes/gato4.png").convert_alpha(), (100, 100))
    return {
        "x": 100,
        "y": 500,
        "velocidad": 60,
        "imagen": imagen
    }

def actualizar_personaje(pantalla, estado, teclas):
    if teclas[pygame.K_LEFT]:
        estado["x"] -= estado["velocidad"]
    if teclas[pygame.K_RIGHT]:
        estado["x"] += estado["velocidad"]
    if teclas[pygame.K_UP]:
        estado["y"] -= estado["velocidad"]
    if teclas[pygame.K_DOWN]:
        estado["y"] += estado["velocidad"]

    if estado["x"] < 0:
        estado["x"] = 0
    if estado["x"] > ANCHO - estado["imagen"].get_width():
        estado["x"] = ANCHO - estado["imagen"].get_width()

    if estado["y"] < 0:
        estado["y"] = 0
    if estado["y"] > ALTO - estado["imagen"].get_height():
        estado["y"] = ALTO - estado["imagen"].get_height()    

    pantalla.blit(estado["imagen"], (estado["x"], estado["y"]))

    return estado