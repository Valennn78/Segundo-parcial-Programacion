import pygame
# ----------------- SONIDO -----------------
pygame.mixer.init()  # Inicializa el motor de sonido
sonido_ambiente = pygame.mixer.Sound("sonidos/ambiente.wav")
sonido_error = pygame.mixer.Sound("sonidos/error.wav")
sonido_correcto = pygame.mixer.Sound("sonidos/correcto.wav")
sonido_ganaste = pygame.mixer.Sound("sonidos/ganaste.wav")
sonido_grito = pygame.mixer.Sound("sonidos/perdiste_grito.wav")


