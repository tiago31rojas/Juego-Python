import pygame

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 65
        self.alto = 60
        self.velocidad = 5
        self.color = (0, 0, 0, 0)  
        self.imagen = pygame.image.load("C:\\Users\\Tiago\\Desktop\\juego.py\\enemigo-removebg-preview.png")
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        self.vida = 3
        self.puntos = 2 
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        pygame.draw.rect(ventana, self.color, self.rect)  
        ventana.blit(self.imagen, (self.x, self.y))
         
    def movimiento(self):
        self.y += self.velocidad

class Jefe(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = 20
        self.vida_max = 20
        self.ancho = 100
        self.alto = 80
        self.velocidad = 2
        self.puntos = 50 
        self.imagen_jefe = pygame.image.load("C:\\Users\\Tiago\\Desktop\\juego.py\\Jefe.png")
        self.imagen_jefe = pygame.transform.scale(self.imagen_jefe, (self.ancho, self.alto))
        self.color = (0, 0, 0, 0) 

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        pygame.draw.rect(ventana, self.color, self.rect)  
        ventana.blit(self.imagen_jefe, (self.x, self.y))