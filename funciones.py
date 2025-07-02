
import random
import pygame
import sys
from constantes import *
from sonidos import *
from personaje import *
from imagenes import *

pygame.mixer.init()#inicializon de mixer


# ----------------- BUCLE PRINCIPAL -----------------
def jugar(pantalla):
    personaje_estado = crear_personaje() # Creamos el personaje

    palabra = elegir_palabra(obtener_lista_palabras("palabras.txt")) # seleccion de palabra aleatoria desde archivo txt
    letras_utilizadas = [] # Lista inicial de letras ingresadas
    errores = 0 # Contador de errores
    max_errores = 6 # Comparador de errores

    reloj = pygame.time.Clock() # Creamos una variable de tipo Clock a fin de medir los fps
    sonido_ambiente.play(-1) # inicializacion de sonido de ambiente
    
    jugando = True # Inicializamos bandera Jugando para el ingreso y salida deo bucle posteriormente
    while jugando:
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get(): # captura los eventos 
            if evento.type == pygame.QUIT: # si se cierra la ventana 
                pygame.quit() # sale de pygame 
                sys.exit()
            if evento.type == pygame.KEYDOWN: # si se presiona una tecla 
                letra = evento.unicode.upper() # Convierte la tecla en mayus 
                if letra.isalpha(): # Verifica que sea una letra 
                    resultado = verificar_letra(letra, palabra, letras_utilizadas) # Llamamos a funcion verificar letra
                    if resultado is False:
                        errores += 1 # aumenta el contador de errores 
                        sonido_error.play() # Reproducimos sonido
                    elif resultado is True:
                        sonido_correcto.play() # Reproducimos sonido 

        dibujar_juego(pantalla, palabra, letras_utilizadas, errores) # Llamamos a dibujar juego
        
        actualizar_personaje(pantalla, personaje_estado, teclas)

        pygame.display.flip() # Actualizamos pantalla
        reloj.tick(60) # limitamos la cantidad de frames por segundo a 60

        # VALIDAMOS SI GANO
        gano = True # si gano 
        for letra in palabra: # letras en palabras 
            if letra not in letras_utilizadas: # si hay una letra no adivinada 
                gano = False
                break
        # GANÓ
        if gano:
            sonido_ganaste.play() # Reproducimos sonido
            # Mostrar una imagen centrada en la pantalla (más grande para un mensaje especial)
            try:
                imagen_centrada = pygame.transform.scale(pygame.image.load("imagenes/you_win.png").convert_alpha(), (350, 350))
                pantalla.blit(imagen_centrada, (225, 240))
                pygame.display.flip()#actualizamos pantalla
            except pygame.error: print("No se pudo cargar imagen.")

            pygame.time.delay(4000) # Pausa de 4 segundos
            jugando = False # finaliza el juego 

        # PERDIO
        if errores >= max_errores:
            try:
                # Mostrar screamer en toda la pantalla
                sonido_grito.play() # Reproducimos sonido de screamer
                screamer_img = pygame.transform.scale(pygame.image.load("imagenes/screamer.png").convert_alpha(), (ANCHO, ALTO)) # Cargamos y escalamos la imagen de derrota al tamaño de la pantalla
                pantalla.blit(screamer_img, (0, 0)) # Pegamos la variable que contiene la imagen por sobre la pantalla
                
                # carga y muestra imagen de perdiste 
                you_lost_img = pygame.transform.scale(pygame.image.load("imagenes/you_lost.png").convert_alpha(), (350, 120)) # Mostramos imagen de perdiste debajo y por encima de screamer img
                pantalla.blit(you_lost_img, (225, 240))
                pygame.display.flip()# actualiza la pantalla 
                
            except pygame.error:
                print("No se pudo cargar imagen'.")
            pygame.time.delay(4000) # Pausa de 4 segundos
            errores = 0
            jugando = False # Salida del bucle principal
# ----------------- CARGAR PALABRAS DESDE ARCHIVO -----------------

def obtener_lista_palabras(archivo):
    with open(archivo, 'r') as archivo_abierto: # abre el archivo en modo lectura
        palabras = archivo_abierto.read().splitlines()# lee linea por linea y saca los saltos de línea
    return palabras # devuelve la lista de palabras 

# ----------------- ELEGIR PALABRA AL AZAR -----------------
def elegir_palabra(lista):
    seleccion_aleatoria = random.choice(lista) # selecciona una palabra aleatoria 
    return seleccion_aleatoria.upper()# devuelve la palabra con mayus

# ----------------- DIBUJAR ESTRUCTURA DEL AHORCADO -----------------
def dibujar_estructura(pantalla):

    # CON OFFSETS DIBUJAMOS  LA ESTRUCTURA, CON ESTO TENEMOS UN MARGEN AL REDEDOR DE LA PANTALLA.

    # BASE DE LA ESTRUCTURA
    pygame.draw.rect(pantalla, SOMBRA, (48 + OFFSET_X, 448 + OFFSET_Y, 154, 16)) # DETALLAMOS UNA SOMBRA DE LA BASE
    pygame.draw.rect(pantalla, MADERA_CLARA, (50 + OFFSET_X, 450 + OFFSET_Y, 150, 10))  # DIBUJAMOS LA BASE DE LA ESTRUCTURA CON MADERA CLARA

    # POSTE 
    pygame.draw.rect(pantalla, SOMBRA, (122 + OFFSET_X, 98 + OFFSET_Y, 11, 354)) # DETALLAMOS LA SOMBRA DEL POSTE PRINCIPAL
    pygame.draw.rect(pantalla, MADERA_OSCURA, (125 + OFFSET_X, 100 + OFFSET_Y, 10, 350)) # DIBUJAMOS EL POSTE PRINCIPAL CON MADERA OSCURA

    # BRAZO PARA LA SOGA
    pygame.draw.rect(pantalla, MADERA_OSCURA, (125 + OFFSET_X, 100 + OFFSET_Y, 125, 10)) # DIBUJAMOS EL BRAZO DE QUE SOSTENDRA LA SOGA

    # VIGA DIAGONAL 
    pygame.draw.polygon(pantalla, MADERA_CLARA, 
        [(125 + OFFSET_X, 130 + OFFSET_Y),
        (160 + OFFSET_X, 100 + OFFSET_Y),
        (165 + OFFSET_X, 105 + OFFSET_Y),
        (130 + OFFSET_X, 135 + OFFSET_Y)])

    # SOGA
    pygame.draw.line(pantalla, (230, 200, 150), (250 + OFFSET_X, 110 + OFFSET_Y), (250 + OFFSET_X, 170 + OFFSET_Y), 4)
    pygame.draw.circle(pantalla, (200, 160, 100), (250 + OFFSET_X, 170 + OFFSET_Y), 5)

# ----------------- DIBUJAR PARTES DEL CUERPO -----------------
def dibujar_cuerpo(errores):

    pantalla = pygame.display.get_surface()
    centro_cabeza = (250 + OFFSET_X, 190 + OFFSET_Y)

    if errores >= 1:
        # Cabeza (centrada)
        pantalla.blit(cabeza_img, (centro_cabeza[0] - 25, centro_cabeza[1] - 20))  

    if errores >= 2:
        # Cuerpo (debe salir desde abajo de la cabeza)
        pantalla.blit(torso_img, (centro_cabeza[0] - 27, centro_cabeza[1] + 30))  

    if errores >= 3:
        # Brazo izquierdo
        pantalla.blit(brazo_izquierdo_img, (centro_cabeza[0] - 75, centro_cabeza[1] + 40)) 

    if errores >= 4:
        # Brazo derecho
        pantalla.blit(Brazo_derecho_img, (centro_cabeza[0] + 32, centro_cabeza[1] + 37))

    if errores >= 5:
        # Pierna izquierda
        pantalla.blit(pierna_izquierda_img, (centro_cabeza[0] - 54, centro_cabeza[1] + 108))

    if errores >= 6:
        # Pierna derecha
        pantalla.blit(pierna_derecha_img, (centro_cabeza[0], centro_cabeza[1] + 108)) 

# ----------------- CARGAR Y DIBUJAR LOGO -----------------

def logo(pantalla):
    try:
        # Cargar la imagen del logo
        imagen_logo = pygame.transform.scale(pygame.image.load("imagenes/marca.png").convert_alpha(), (130, 130)) # Escalar a tamaño más grande
       
        pantalla.blit(imagen_logo, (20, 20)) # presenta la imagen en pantalla 
    
    except pygame.error:
        print("No se pudo cargar imagen")

# ----------------- DIBUJAR JUEGO EN PANTALLA -----------------
def dibujar_juego(pantalla, palabra, letras_utilizadas, errores):
    # Fondo
    try:
         #Intenta cargar la imagen 
        fondo = pygame.transform.scale(pygame.image.load("imagenes/FONDO.JPG").convert(), (ANCHO, ALTO)) #Escala al tamaño de la ventana 
        
        pantalla.blit(fondo, (0, 0))# presenta imagen 
        
    except pygame.error:
        pantalla.fill((255, 255, 255))  # Blanco si no se encuentra la imagen

    # Título
    pygame.display.set_caption(TITULO) # Establece un titulo en la ventana 

    # Dibujar elementos visuales

    dibujar_estructura(pantalla) # Dibuja horca 
    dibujar_cuerpo(errores) # Dibuja cuerpo segun los errores 
    logo(pantalla) # Dibuja el logo 

    # Mostrar palabra con guiones
    fuente = pygame.font.SysFont(None, 60)
    texto = ""
    for letra in palabra:
        if letra in letras_utilizadas:
            texto += letra + " " # muestra letras adivinadas 
        else:
            texto += "_ " # muestra guion bajon

    render = fuente.render(texto, True, NEGRO)
    pantalla.blit(render, (300,520))

    # Mostrar letras incorrectas
    letras_incorrectas = []

    for letra in letras_utilizadas:
        if letra not in palabra:
            letras_incorrectas.append(letra)
            
    fuente_pequeña = pygame.font.SysFont(None, 36)
    texto_incorrectas = fuente_pequeña.render("Incorrectas: " + " ".join(letras_incorrectas), True, ROJO)
    pantalla.blit(texto_incorrectas, (50, 570))
    # Llenar fondo, mostrar palabra oculta, letras ingresadas y dibujar estructura y cuerpo

# ----------------- VERIFICAR LETRA -----------------
def verificar_letra(letra, palabra, letras_utilizadas):
    if letra not in letras_utilizadas: #solo si no se uso antes 
        letras_utilizadas.append(letra)# la agrega a la lista 
        return letra in palabra#devuelve true si esta en la palabra 
    return None  #si ya se uso no hace nada






















































'''
# ----------------- BUCLE PRINCIPAL -----------------
def jugar(pantalla):
    palabra = elegir_palabra(obtener_lista_palabras("palabras.txt")) # seleccion de palabra aleatoria desde archivo txt
    letras_utilizadas = [] # Lista inicial de letras ingresadas
    errores = 0 # Contador de errores
    max_errores = 6 # Comparador de errores

    reloj = pygame.time.Clock() # Creamos una variable de tipo Clock a fin de medir los frames
    sonido_ambiente.play(-1) # inicializacion de sonido de ambiente
    
    jugando = True # Inicializamos bandera Jugando para el ingreso y salida deo bucle posteriormente
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                letra = evento.unicode.upper()
                if letra.isalpha():
                    resultado = verificar_letra(letra, palabra, letras_utilizadas) # Llamamos a funcion verificar letra
                    if resultado is False:
                        errores += 1
                        sonido_error.play() # Reproducimos sonido
                    elif resultado is True:
                        sonido_correcto.play() # Reproducimos sonido 

        dibujar_juego(pantalla, palabra, letras_utilizadas, errores) # Llamamos a dibujar juego
        pygame.display.flip() # Actualizamos pantalla
        reloj.tick(60) # limitamos la cantidad de frames por segundo a 60

        # VALIDAMOS SI GANO
        gano = True
        for letra in palabra:
            if letra not in letras_utilizadas:
                gano = False
                break
        # GANÓ
        if gano:
            sonido_ganaste.play() # Reproducimos sonido
            # Mostrar una imagen centrada en la pantalla (más grande para un mensaje especial)
            try:
                imagen_centrada = pygame.transform.scale(pygame.image.load("imagenes/you_win.png").convert_alpha(), (350, 350))
                x_centrada = ANCHO // 2 - imagen_centrada.get_width() // 2
                y_centrada = ALTO // 2 - imagen_centrada.get_height() // 2
                pantalla.blit(imagen_centrada, (x_centrada, y_centrada))
                pygame.display.flip()
            except pygame.error: print("No se pudo cargar imagen.")

            pygame.time.delay(4000) # Pausa de 4 segundos
            jugando = False

        # PERDIO
        if errores >= max_errores:
            try:
                # Mostrar screamer en toda la pantalla
                sonido_grito.play() # Reproducimos sonido de screamer
                screamer_img = pygame.transform.scale(pygame.image.load("imagenes/screamer.png").convert_alpha(), (ANCHO, ALTO)) # Cargamos y escalamos la imagen de derrota al tamaño de la pantalla
                pantalla.blit(screamer_img, (0, 0)) # Pegamos la variable que contiene la imagen por sobre la pantalla
                you_lost_img = pygame.transform.scale(pygame.image.load("imagenes/you_lost.png").convert_alpha(), (350, 120)) # Mostramos imagen de perdiste debajo y por encima de screamer img
                x_lost = ANCHO // 2 - you_lost_img.get_width() // 2
                y_lost = ALTO - you_lost_img.get_height() - 30
                pantalla.blit(you_lost_img, (x_lost, y_lost))
                pygame.display.flip() 
            except pygame.error:
                print("No se pudo cargar imagen'.")
            pygame.time.delay(4000) # Pausa de 4 segundos
            jugando = False # Salida del bucle principal

# ----------------- CARGAR PALABRAS DESDE ARCHIVO -----------------

def obtener_lista_palabras(archivo):
    # Abrir el archivo en modo lectura
    with open(archivo, 'r') as archivo_abierto:
        # Leer todas las líneas y quitar los saltos de línea
        palabras = archivo_abierto.read().splitlines()
    return palabras

# ----------------- ELEGIR PALABRA AL AZAR -----------------
def elegir_palabra(lista):
    seleccion_aleatoria = random.choice(lista)
    
    # Elegir una palabra aleatoria de la lista y convertirla a mayúsculas
    return seleccion_aleatoria.upper()

# ----------------- DIBUJAR ESTRUCTURA DEL AHORCADO -----------------
def dibujar_estructura(pantalla):

    # CON OFFSETS DIBUJAMOS  LA ESTRUCTURA, CON ESTO TENEMOS UN MARGEN AL REDEDOR DE LA PANTALLA.

    # BASE DE LA ESTRUCTURA
    pygame.draw.rect(pantalla, SOMBRA, (48 + OFFSET_X, 448 + OFFSET_Y, 154, 16)) # DETALLAMOS UNA SOMBRA DE LA BASE
    pygame.draw.rect(pantalla, MADERA_CLARA, (50 + OFFSET_X, 450 + OFFSET_Y, 150, 10))  # DIBUJAMOS LA BASE DE LA ESTRUCTURA CON MADERA CLARA

    # POSTE 
    pygame.draw.rect(pantalla, SOMBRA, (122 + OFFSET_X, 98 + OFFSET_Y, 11, 354)) # DETALLAMOS LA SOMBRA DEL POSTE PRINCIPAL
    pygame.draw.rect(pantalla, MADERA_OSCURA, (125 + OFFSET_X, 100 + OFFSET_Y, 10, 350)) # DIBUJAMOS EL POSTE PRINCIPAL CON MADERA OSCURA

    # BRAZO PARA LA SOGA
    pygame.draw.rect(pantalla, MADERA_OSCURA, (125 + OFFSET_X, 100 + OFFSET_Y, 125, 10)) # DIBUJAMOS EL BRAZO DE QUE SOSTENDRA LA SOGA

    # VIGA DIAGONAL 
    pygame.draw.polygon(pantalla, MADERA_CLARA, 
        [(125 + OFFSET_X, 130 + OFFSET_Y),
        (160 + OFFSET_X, 100 + OFFSET_Y),
        (165 + OFFSET_X, 105 + OFFSET_Y),
        (130 + OFFSET_X, 135 + OFFSET_Y)])

    # SOGA
    pygame.draw.line(pantalla, (230, 200, 150), (250 + OFFSET_X, 110 + OFFSET_Y), (250 + OFFSET_X, 170 + OFFSET_Y), 4)
    pygame.draw.circle(pantalla, (200, 160, 100), (250 + OFFSET_X, 170 + OFFSET_Y), 5)

# ----------------- DIBUJAR PARTES DEL CUERPO -----------------
def dibujar_cuerpo(errores):
    OFFSET_X = 50
    OFFSET_Y = 30

    pantalla = pygame.display.get_surface()
    centro_cabeza = (250 + OFFSET_X, 190 + OFFSET_Y)

    if errores >= 1:
        # Cabeza (centrada)
        pantalla.blit(CABEZA_IMG, (centro_cabeza[0] - 25, centro_cabeza[1] - 20))  # 40x40 imagen

    if errores >= 2:
        # Cuerpo (debe salir desde abajo de la cabeza)
        pantalla.blit(TORSO_IMG, (centro_cabeza[0] - 27, centro_cabeza[1] + 30))  # 20x70 imagen

    if errores >= 3:
        # Brazo izquierdo
        pantalla.blit(BRAZO_IZQUIERDO_IMG, (centro_cabeza[0] - 75, centro_cabeza[1] + 40))  # 30x30 imagen

# ----------------- DIBUJAR PARTES DEL CUERPO -----------------

def logo(pantalla):
    try:
        # Cargar la imagen del logo
        imagen_logo = pygame.image.load("imagenes/marca.png").convert_alpha()
        
        # Escalar a tamaño más grande
        imagen_logo = pygame.transform.scale(imagen_logo, (150, 150))

        # Posición: arriba a la izquierda (con margen)
        x = 20
        y = 20

        pantalla.blit(imagen_logo, (x, y))
    
    except pygame.error:
        print("No se pudo cargar 'marca.png'. Verificá que esté en la carpeta del proyecto.")

# ----------------- DIBUJAR JUEGO EN PANTALLA -----------------
def dibujar_juego(pantalla, palabra, letras_utilizadas, errores):
    # Fondo
    try:
        fondo = pygame.image.load("imagenes/FONDO.JPG").convert()
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
    except pygame.error:
        pantalla.fill((255, 255, 255))  # Blanco si no se encuentra la imagen

    # Título
    pygame.display.set_caption(TITULO)

    # Dibujar elementos visuales
    dibujar_estructura(pantalla)
    dibujar_cuerpo(errores)
    logo(pantalla)

    # Mostrar palabra con guiones
    fuente = pygame.font.SysFont(None, 60)
    texto = ""
    for letra in palabra:
        if letra in letras_utilizadas:
            texto += letra + " "
        else:
            texto += "_ "

    render = fuente.render(texto.strip(), True, NEGRO)
    pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, 520))

    # Mostrar letras incorrectas
    letras_incorrectas = [l for l in letras_utilizadas if l not in palabra]
    fuente_pequeña = pygame.font.SysFont(None, 36)
    texto_incorrectas = fuente_pequeña.render("Incorrectas: " + " ".join(letras_incorrectas), True, ROJO)
    pantalla.blit(texto_incorrectas, (50, 570))
    # Llenar fondo, mostrar palabra oculta, letras ingresadas y dibujar estructura y cuerpo

# ----------------- VERIFICAR LETRA -----------------
def verificar_letra(letra, palabra, letras_utilizadas):
    if letra not in letras_utilizadas:
        letras_utilizadas.append(letra)
        return letra in palabra
    return None  # Ya fue usada

'''