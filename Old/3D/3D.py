import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# Parámetros
WIDTH = 800
HEIGHT = 600
FPS = 30
NUM_INDIVIDUOS = 10
PASILLO_OFFSET = -50
PASILLO_ANCHO = 100
PASILLO_ALTO = 100
PASILLO_PROFUNDIDAD = 300

class Individuo:
    def __init__(self, x, y, z, objetivo, velocidad):
        self.pos = np.array([x, y, z], dtype=float)
        self.objetivo = objetivo
        self.velocidad = velocidad

    def update(self, dt):
        direccion = self.objetivo - self.pos
        distancia = np.linalg.norm(direccion)
        if distancia > 1:
            direccion = direccion / distancia
            nueva_pos = self.pos + direccion * self.velocidad * dt
            if PASILLO_OFFSET < nueva_pos[0] < PASILLO_OFFSET + PASILLO_ANCHO and \
               PASILLO_OFFSET < nueva_pos[1] < PASILLO_OFFSET + PASILLO_ALTO and \
               0 < nueva_pos[2] < PASILLO_PROFUNDIDAD:
                self.pos = nueva_pos

def draw_individuo(individuo):
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(individuo.pos[0], individuo.pos[1], -individuo.pos[2])
    gluSphere(gluNewQuadric(), 2, 10, 10)
    glPopMatrix()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulación de pasillo en 3D con paredes")
    clock = pygame.time.Clock()

    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 500.0)
    glTranslatef(0.0, 0.0, -200)

    individuos = []
    for _ in range(NUM_INDIVIDUOS):
        x = random.uniform(PASILLO_OFFSET, PASILLO_OFFSET + PASILLO_ANCHO)
        y = random.uniform(PASILLO_OFFSET, PASILLO_OFFSET + PASILLO_ALTO)
        z = random.uniform(0, PASILLO_PROFUNDIDAD)
        objetivo = np.array([random.uniform(PASILLO_OFFSET, PASILLO_OFFSET + PASILLO_ANCHO),
                             random.uniform(PASILLO_OFFSET, PASILLO_OFFSET + PASILLO_ALTO),
                             random.uniform(0, PASILLO_PROFUNDIDAD)])
        velocidad = random.uniform(50, 150)
        individuos.append(Individuo(x, y, z, objetivo, velocidad))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Habilitar el buffer de profundidad
        glEnable(GL_DEPTH_TEST)

        # Actualizar y dibujar individuos
        for individuo in individuos:
            individuo.update(dt)
            draw_individuo(individuo)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
