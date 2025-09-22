import pygame
from personaje import Cuadrado
from enemigo import Enemigo , Jefe
from balas import Balas
from item import Item
import random
import json
from datetime import datetime

pygame.init()

pygame.mixer.init()

ANCHO = 1000
ALTO = 900
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
FPS = 60
FUENTE = pygame.font.SysFont("Game Font", 25)
FUENTE_MENSAJE = pygame.font.SysFont("Game Font", 24)
FUENTE_PEQUENA = pygame.font.SysFont("Game Font", 25)
pygame.display.set_caption("Mi Juego - Space Shooter")


SONIDO_DISPARO = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonidoBala1s.mp3")
SONIDO_INICIO = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonido Start.mp3")
SONIDO_MUERTE = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonidoExplosion.mp3")

SONIDO_ITEM = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonidoBala1s.mp3")
SONIDO_NIVEL = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonidoBala1s.mp3")
SONIDO_ESCUDO = pygame.mixer.Sound("C:\\Users\\Tiago\\Documents\\Audacity\\sonidoBala1s.mp3")

SONIDO_INICIO.play()


jugando = True
pausado = False
jefe_activo = False

reloj = pygame.time.Clock()

vidas = 3
puntaje = 0
nivel = 1
puntos_para_siguiente_nivel = 100
enemigos_eliminados = 0
mejor_puntuacion = 0

tiempo_pasado = 0
tiempo_entre_enemigos = 500
tiempo_entre_enemigos_base = 1000


mensaje_item = ""
tiempo_mensaje = 0
duracion_mensaje = 2000

tiempo_velocidad_aumentada = 0
duracion_velocidad = 25000
velocidad_original = 500
velocidad_activa = False
velocidad_bonus = 0

escudo_activo = False
tiempo_escudo = 0
duracion_escudo = 15000

arma_especial_activa = False
tiempo_arma_especial = 0
duracion_arma_especial = 20000

logros = {
    "primer_muerte": False,
    "100_puntos": False,
    "nivel_5": False,
    "sin_danio": False,
    "primer_jefe": False
}

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.tamaño = random.randint(2, 8)
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.vida = 30

particulas = []

cuadrado = Cuadrado(ANCHO/2, ALTO-65)

enemigos = []
balas = []
items = []

ultima_bala = 0
tiempo_entre_balas = 400

tiempo_ultimo_item = 0
tiempo_entre_items = 10000  

try:
    with open('mejor_puntuacion.txt', 'r') as f:
        mejor_puntuacion = int(f.read())
except:
    mejor_puntuacion = 0

def crear_bala():
    global ultima_bala

    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        if arma_especial_activa:
            for offset in [-20, 0, 20]:
                balas.append(Balas(cuadrado.rect.centerx + offset, cuadrado.rect.centery))
        else:
            balas.append(Balas(cuadrado.rect.centerx, cuadrado.rect.centery))
        
        ultima_bala = pygame.time.get_ticks()
        SONIDO_DISPARO.play()

def gestionar_teclas(teclas):
    global pausado
    
    if teclas[pygame.K_a]:
        if cuadrado.x >= 0:
            cuadrado.x -= cuadrado.velocidad
    if teclas[pygame.K_d]:
        if cuadrado.x + cuadrado.ancho <= ANCHO:
            cuadrado.x += cuadrado.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()
    if teclas[pygame.K_p]:
        pausado = not pausado
        pygame.time.delay(200)

def mostrar_menu_pausa():
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    VENTANA.blit(s, (0, 0))
    
    titulo = FUENTE.render("JUEGO EN PAUSA", True, "white")
    VENTANA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
    
    textos = [
        f"Puntuación: {puntaje}",
        f"Mejor Puntuación: {mejor_puntuacion}",
        f"Nivel: {nivel}",
        f"Vidas: {vidas}",
        f"Enemigos eliminados: {enemigos_eliminados}",
        "",
        "Presiona P para continuar"
    ]
    
    for i, texto in enumerate(textos):
        texto_render = FUENTE_MENSAJE.render(texto, True, "white")
        VENTANA.blit(texto_render, (ANCHO//2 - 150, 200 + i*40))

def verificar_logros():
    global logros, mensaje_item, tiempo_mensaje
    
    if puntaje >= 100 and not logros["100_puntos"]:
        logros["100_puntos"] = True
        mensaje_item = "¡LOGRO: 100 PUNTOS!"
        tiempo_mensaje = pygame.time.get_ticks()
    
    if nivel >= 5 and not logros["nivel_5"]:
        logros["nivel_5"] = True
        mensaje_item = "¡LOGRO: NIVEL 5!"
        tiempo_mensaje = pygame.time.get_ticks()
    
    if jefe_activo and not logros["primer_jefe"]:
        logros["primer_jefe"] = True
        mensaje_item = "¡LOGRO: PRIMER JEFE!"
        tiempo_mensaje = pygame.time.get_ticks()

def evitar_superposicion(nuevo_obj, lista_objetos, min_distancia=50):
    for obj in lista_objetos:
        distancia = ((nuevo_obj.x - obj.x)**2 + (nuevo_obj.y - obj.y)**2)**0.5
        if distancia < min_distancia:
            return False
    return True

while jugando and vidas > 0:
    tiempo_actual = pygame.time.get_ticks()
    
    if pausado:
        mostrar_menu_pausa()
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                pausado = False
        
        continue
    
    tiempo_pasado += reloj.tick(FPS)

    if velocidad_activa and tiempo_actual - tiempo_velocidad_aumentada > duracion_velocidad:
        tiempo_entre_balas = velocidad_original
        velocidad_activa = False
        velocidad_bonus = 0
        mensaje_item = "VELOCIDAD NORMAL"
        tiempo_mensaje = tiempo_actual

    if escudo_activo and tiempo_actual - tiempo_escudo > duracion_escudo:
        escudo_activo = False
        mensaje_item = "ESCUDO DESACTIVADO"
        tiempo_mensaje = tiempo_actual

    if arma_especial_activa and tiempo_actual - tiempo_arma_especial > duracion_arma_especial:
        arma_especial_activa = False
        mensaje_item = "ARMA NORMAL"
        tiempo_mensaje = tiempo_actual

    if puntaje >= puntos_para_siguiente_nivel:
        nivel += 1
        puntos_para_siguiente_nivel += 150
        tiempo_entre_enemigos_base = max(200, tiempo_entre_enemigos_base - 50)
        mensaje_item = f"¡NIVEL {nivel} ALCANZADO!"
        tiempo_mensaje = tiempo_actual
        SONIDO_NIVEL.play()

    if nivel % 3 == 0 and not jefe_activo and len([e for e in enemigos if isinstance(e, Jefe)]) == 0:
        nuevo_jefe = Jefe(ANCHO//2, -150)
        enemigos.append(nuevo_jefe)
        jefe_activo = True
        mensaje_item = "¡JEFE INCOMING!"
        tiempo_mensaje = tiempo_actual

    if tiempo_pasado > tiempo_entre_enemigos:
        intentos = 0
        while intentos < 10: 
            x_pos = random.randint(50, ANCHO-50)
            nuevo_enemigo = Enemigo(x_pos, -100)
            
            if evitar_superposicion(nuevo_enemigo, enemigos + items, 70):
                enemigos.append(nuevo_enemigo)
                tiempo_pasado = 0
                tiempo_entre_enemigos = random.randint(50, tiempo_entre_enemigos_base)
                if tiempo_entre_enemigos_base > 200:
                    tiempo_entre_enemigos_base -= 20
                break
            intentos += 1

    if (tiempo_actual - tiempo_ultimo_item > tiempo_entre_items and 
        random.randint(1, 200) == 1):  
        intentos = 0
        while intentos < 10:
            x_pos = random.randint(50, ANCHO-50)
            nuevo_item = Item(x_pos, -50)
            
            if evitar_superposicion(nuevo_item, enemigos + items, 80):
                items.append(nuevo_item)
                tiempo_ultimo_item = tiempo_actual
                break
            intentos += 1

    for particula in particulas[:]:
        particula.vida -= 1
        particula.x += particula.vel_x
        particula.y += particula.vel_y
        if particula.vida <= 0:
            particulas.remove(particula)

    eventos = pygame.event.get()
    teclas = pygame.key.get_pressed()

    texto_vidas = FUENTE.render(f"Vidas: {vidas}", True, "white")
    texto_puntos = FUENTE.render(f"Puntos: {puntaje}", True, "white")
    texto_nivel = FUENTE.render(f"Nivel: {nivel}", True, "white")

    gestionar_teclas(teclas)
    
    for evento in eventos:
        if evento.type == pygame.QUIT:
            jugando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
            pausado = not pausado

    VENTANA.fill("black") 
    
    pygame.draw.rect(VENTANA, "red", (20, ALTO - 30, 200, 20))
    pygame.draw.rect(VENTANA, "green", (20, ALTO - 30, 200 * (vidas/3), 20))
    
    progreso = min(100, (puntaje / puntos_para_siguiente_nivel) * 100)
    pygame.draw.rect(VENTANA, "blue", (ANCHO - 220, 60, 200, 15))
    pygame.draw.rect(VENTANA, "cyan", (ANCHO - 220, 60, 200 * (progreso/100), 15))
    
    if velocidad_activa:
        tiempo_restante = (duracion_velocidad - (tiempo_actual - tiempo_velocidad_aumentada)) // 1000
        texto_velocidad = FUENTE.render(f"{tiempo_restante}s", True, "yellow")
        VENTANA.blit(texto_velocidad, (ANCHO - 120, 20))

    if escudo_activo:
        tiempo_restante = (duracion_escudo - (tiempo_actual - tiempo_escudo)) // 1000
        texto_escudo = FUENTE.render(f"{tiempo_restante}s", True, "cyan")
        VENTANA.blit(texto_escudo, (ANCHO - 120, 70))

    if arma_especial_activa:
        tiempo_restante = (duracion_arma_especial - (tiempo_actual - tiempo_arma_especial)) // 1000
        texto_arma = FUENTE.render(f"{tiempo_restante}s", True, "orange")
        VENTANA.blit(texto_arma, (ANCHO - 120, 120))

    for particula in particulas:
        pygame.draw.circle(VENTANA, particula.color, (int(particula.x), int(particula.y)), particula.tamaño)

    for item in items[:]:  
        item.dibujar(VENTANA)
        item.movimiento()

    for enemigo in enemigos[:]: 
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()

    for bala in balas[:]:  
        bala.dibujar(VENTANA)
        bala.movimiento()

    cuadrado.dibujar(VENTANA)
    
    if escudo_activo:
        pygame.draw.circle(VENTANA, "cyan", (cuadrado.rect.centerx, cuadrado.rect.centery), 40, 3)

    for enemigo in enemigos:
        if isinstance(enemigo, Jefe):
            ancho_barra = 100
            pygame.draw.rect(VENTANA, "red", (enemigo.x, enemigo.y - 25, ancho_barra, 8))
            pygame.draw.rect(VENTANA, "green", (enemigo.x, enemigo.y - 25, ancho_barra * (enemigo.vida/enemigo.vida_max), 8))

    for enemigo in enemigos[:]: 
        if pygame.Rect.colliderect(cuadrado.rect, enemigo.rect):
            if escudo_activo:
                for _ in range(10):
                    particulas.append(Particula(enemigo.x, enemigo.y, "cyan"))
                if enemigo in enemigos:
                    enemigos.remove(enemigo)
            else:
                vidas -= 1
                if enemigo in enemigos:
                    enemigos.remove(enemigo)
            continue

        if enemigo.y > ALTO:
            puntaje += 1
            if enemigo in enemigos:
                enemigos.remove(enemigo)
            continue

        for bala in balas[:]:  
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                enemigo.vida -= 1
                if bala in balas:
                    balas.remove(bala)
                
                for _ in range(5):
                    particulas.append(Particula(enemigo.x, enemigo.y, "orange"))
                
                if enemigo.vida <= 0: 
                    SONIDO_MUERTE.play()
                    enemigos_eliminados += 1
                    
                    for _ in range(15):
                        particulas.append(Particula(enemigo.x, enemigo.y, "red"))
                    
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                    
                    puntaje += enemigo.puntos          

                    if isinstance(enemigo, Jefe):
                        jefe_activo = False
                        for _ in range(2):  
                            item_x = enemigo.x + random.randint(-50, 50)
                            item_y = enemigo.y + random.randint(-50, 50)
                            nuevo_item = Item(item_x, item_y)
                            items.append(nuevo_item)
                    elif random.randint(1, 8) == 1: 
                        item_x = enemigo.x + enemigo.ancho/2 - 15
                        item_y = enemigo.y + enemigo.alto/2
                        nuevo_item = Item(item_x, item_y)
                        items.append(nuevo_item)
                    
                    break

    for bala in balas[:]:
        if bala.y < 0 and bala in balas:
            balas.remove(bala)

    for item in items[:]:  
        if pygame.Rect.colliderect(item.rect, cuadrado.rect):
            SONIDO_ITEM.play()
            
            if item.tipo == 1:
                vidas += 1
                mensaje_item = "¡VIDA EXTRA!"
                tiempo_mensaje = tiempo_actual
            elif item.tipo == 2:
                if not velocidad_activa:
                    velocidad_bonus = 50
                    tiempo_entre_balas = max(50, velocidad_original - velocidad_bonus)
                    mensaje_item = "¡VELOCIDAD AUMENTADA!"
                    tiempo_velocidad_aumentada = tiempo_actual
                    velocidad_activa = True
                else:
                    tiempo_velocidad_aumentada = tiempo_actual
                    mensaje_item = "¡TIEMPO DE VELOCIDAD EXTENDIDO!"
                
                tiempo_mensaje = tiempo_actual
            elif item.tipo == 3:
                escudo_activo = True
                tiempo_escudo = tiempo_actual
                mensaje_item = "¡ESCUDO ACTIVADO!"
                tiempo_mensaje = tiempo_actual
                SONIDO_ESCUDO.play()
            elif item.tipo == 4:
                arma_especial_activa = True
                tiempo_arma_especial = tiempo_actual
                mensaje_item = "¡ARMA ESPECIAL!"
                tiempo_mensaje = tiempo_actual
            
            if item in items:
                items.remove(item)
            continue
        
        if item.y > ALTO and item in items:
            items.remove(item)
    
    VENTANA.blit(texto_vidas, (20, 20))
    VENTANA.blit(texto_puntos, (20, 60))
    VENTANA.blit(texto_nivel, (20, 100))
    
    if mejor_puntuacion > 0:
        texto_mejor = FUENTE_PEQUENA.render(f"Mejor: {mejor_puntuacion}", True, "gold")
        VENTANA.blit(texto_mejor, (ANCHO - 150, 20))
    
    if tiempo_actual - tiempo_mensaje < duracion_mensaje and mensaje_item:
        texto_mensaje = FUENTE_MENSAJE.render(mensaje_item, True, "yellow")
        VENTANA.blit(texto_mensaje, (ANCHO//2 - texto_mensaje.get_width()//2, 100))
    
    verificar_logros()

    pygame.display.update()

if puntaje > mejor_puntuacion:
    mejor_puntuacion = puntaje
    with open('mejor_puntuacion.txt', 'w') as f:
        f.write(str(mejor_puntuacion))

pygame.quit()

nombre = input("Ingresa tu nombre: ")

with open('puntuaciones.txt', 'a') as archivo:
    archivo.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {nombre} - {puntaje} - Nivel {nivel}\n")

print(f"\n=== ESTADÍSTICAS FINALES ===")
print(f"Puntuación: {puntaje}")
print(f"Nivel alcanzado: {nivel}")
print(f"Enemigos eliminados: {enemigos_eliminados}")
print(f"Mejor puntuación: {mejor_puntuacion}")
print("============================")


quit()
