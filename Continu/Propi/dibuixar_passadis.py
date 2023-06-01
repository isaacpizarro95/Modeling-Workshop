import pygame
import sys
from pygame.locals import QUIT
import numpy as np
import math

def dibuixar_passadis_pygame(n, m, passadis, individus, scale_x, scale_y, screen, clock, fps):
    # Definim els colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    color_entrada1 = (0, 0, 255)  # Azul
    color_entrada2 = (255, 0, 0)  # Rojo

    # Asociar las entradas con los colores
    entrades = passadis.get_entrades()
    entrades_colors = {tuple(entrades[0]): color_entrada1, tuple(entrades[1]): color_entrada2}

    # Per parar la simulació quan vulguem
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # "Netejar" pantalla
    screen.fill(white)

    # De igual manera, al dibujar las lineas debes aplicar el factor de escala a las coordenadas
    pygame.draw.line(screen, color_entrada1, tuple(np.array(entrades[0][0]) * [scale_x, scale_y]), tuple(np.array(entrades[0][1]) * [scale_x, scale_y]), 3)
    pygame.draw.line(screen, color_entrada2, tuple(np.array(entrades[1][0]) * [scale_x, scale_y]), tuple(np.array(entrades[1][1]) * [scale_x, scale_y]), 3)
    
    for individu in individus:
        pos = individu.get_posicio()
        
        # El individuo ha salido del mapa
        if pos is None:  continue
        # Obtener el color de la salida de este individuo
        color_individu = entrades_colors[tuple(individu.get_sortida())]
        # Obtener la posición del individuo y aplicar el factor de escala

        pos = (int(pos[0]*scale_x), int(pos[1]*scale_y))
        #print(f"Posición escalada: {pos}")

        radius = individu.get_radi() * min(scale_x, scale_y)
        # Dibujar el individuo con ese color
        pygame.draw.circle(screen, color_individu, pos, 1)  # Dibuja el punto central
        #pygame.draw.circle(screen, color_individu, pos, radius, 1)  # Dibuja la circunferencia

        # Dibujar flecha de dirección
        velocitat = individu.get_velocitat()

        if np.linalg.norm(velocitat) != 0:  # Skip if velocity is zero
            # Normalizar la velocidad para obtener la dirección
            direccion = velocitat / np.linalg.norm(velocitat)

            # Escalar la dirección para que la flecha tenga un tamaño constante
            direccion *= 15

            # Calcular los puntos para el triángulo de la flecha
            punta = tuple(pos + direccion)

            draw_arrow(screen, color_individu, pos, punta, 10)  # Dibuja la flecha
    
    pygame.display.flip()
    clock.tick(fps)  # Limitar a 60 FPS


# Dibuixa la fletxa que indica la direcció de cada individu
def draw_arrow(screen, color, start, end, arrow_head_size):
    dx = int(end[0] - start[0])
    dy = int(end[1] - start[1])
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return
    udx = dx / length
    udy = dy / length
    arrow_head_angle = math.pi / 6
    arrow_tail = (end[0] - udx * arrow_head_size, end[1] - udy * arrow_head_size)
    arrow_left = (
        arrow_tail[0] - udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        arrow_tail[1] + udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    arrow_right = (
        arrow_tail[0] + udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        arrow_tail[1] - udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    pygame.draw.line(screen, color, start, arrow_tail, 1)
    pygame.draw.polygon(screen, color, [end, arrow_left, arrow_right])