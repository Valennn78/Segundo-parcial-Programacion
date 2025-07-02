import pygame
from funciones import *
from constantes import *
from sonidos import *
from personaje import *

# Inicializamos pygame
pygame.init()

# Configuramos la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO)) # asignamos dimensiones con constantes ANCHO, ALTO
icono = pygame.image.load("imagenes/icono.png") # Cargamos el icono del programa
pygame.display.set_icon(icono) #c Desplegamos el icono del programa
       
while True:
    jugar(pantalla)
    pygame.display.flip()


