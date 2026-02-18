# 🚀 Space Shooter - Python & Pygame

Videojuego 2D estilo arcade desarrollado en Python utilizando Pygame.  
El jugador controla una nave que debe eliminar enemigos, sobrevivir oleadas crecientes y enfrentarse a jefes cada ciertos niveles.

---

## 🎮 Características principales

- 🛸 Movimiento lateral del jugador
- 🔫 Sistema de disparo con cooldown
- 👾 Enemigos con vida y puntuación variable
- 🐉 Jefe especial cada 3 niveles
- 📈 Sistema progresivo de niveles y dificultad dinámica
- ❤️ Sistema de vidas
- ⚡ Power-ups:
  - Vida extra
  - Aumento de velocidad de disparo
  - Escudo temporal
  - Arma especial
- 🎯 Sistema de logros
- 🎨 Efectos de partículas para explosiones
- 🔊 Efectos de sonido
- 💾 Guardado automático de mejor puntuación
- 📝 Registro de estadísticas de cada partida

---

## 🧠 Tecnologías utilizadas

- Python 3.11+
- Pygame



## 📂 Estructura del proyecto

├── main.py
├── personaje.py
├── enemigo.py
├── balas.py
├── item.py
├── mejor_puntuacion.txt
├── puntuaciones.txt
├── assets/

Instalar dependencias:

pip install pygame


Ejecutar el juego:

python main.py

🎮 Controles
Tecla	Acción
A	Mover izquierda
D	Mover derecha
SPACE	Disparar
P	Pausar juego
📊 Sistema de progresión

El jugador gana puntos al eliminar enemigos.
Cada cierto puntaje se sube de nivel.
La velocidad y frecuencia de aparición de enemigos aumenta.
Cada 3 niveles aparece un jefe con barra de vida.
Los enemigos pueden soltar objetos especiales.

🏁 Fin de partida

Al finalizar:
Se guarda la mejor puntuación alcanzada.
Se registra la fecha, nombre del jugador, puntaje y nivel.
Se muestran estadísticas finales en consola.

🔮 Mejoras futuras

Pantalla de inicio y menú principal
Pantalla de Game Over visual
Música de fondo
Selector de dificultad
Optimización de assets y rutas relativas
Persistencia en base de datos

👨‍💻 Autor

Proyecto desarrollado como práctica avanzada de programación orientada a objetos, lógica de videojuegos y manejo de eventos en Python.
