import pygame
import random

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.velocidad = 5
        self.tipo = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
        
        if self.tipo == 1:      # Vida
            self.color = "green"
        elif self.tipo == 2:    # Velocidad
            self.color = "blue"
        elif self.tipo == 3:    # Escudo
            self.color = "cyan"
        elif self.tipo == 4:    # Arma especial
            self.color = "purple"
            
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
    
    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) 
        pygame.draw.rect(ventana, self.color, self.rect)
     
    def movimiento(self):
        self.y += self.velocidad