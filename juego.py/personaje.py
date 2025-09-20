import pygame

class Cuadrado:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 10
        self.color = (0, 0, 0, 0)  
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        self.imagen = pygame.image.load("C:\\Users\\Tiago\\Desktop\\juego.py\\fotoNave-removebg-preview.png")
        self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        pygame.draw.rect(ventana, self.color, self.rect)  
        ventana.blit(self.imagen, (self.x, self.y))
         