import pygame
import sys
from pygame.locals import QUIT
import math

def dibuixar_passadis_pygame(n, m, passadis, individus, screen, cell_size, clock):
    
    # Definim colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 165, 0), (128, 0, 128), (165, 42, 42), (255, 255, 0)]

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

    # Dibuixar parets, entrades i obstacles
    parets = passadis.get_parets()
    parets.extend([(0, 0), (0, n - 1), (m - 1, 0), (m - 1, n - 1)])
    vector_entrades = passadis.get_entrades()
    entrades = [e for entrada in vector_entrades for e in entrada]
    obstacles = passadis.get_obstacles()

    for x, y in obstacles:
        pygame.draw.rect(screen, black, (y * cell_size[0], x * cell_size[1], cell_size[0], cell_size[1]))

    for x, y in parets:
        if (x, y) in passadis.get_parets():
            color = gray
        else:
            color = black

        pygame.draw.rect(screen, color, (y * cell_size[0], x * cell_size[1], cell_size[0], cell_size[1]))

        if (x, y) in entrades:
            for entrada in vector_entrades:
                if (x, y) in entrada:
                    color = colors[vector_entrades.index(entrada) % len(colors)]
            pygame.draw.circle(screen, color, (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2), cell_size[0] // 4)

    # Dibuixar individus
    for ind in individus:
        if ind.posicio == None: continue

        objectiu = ind.get_objectiu()
        x, y = ind.get_posicio()
        dx, dy = ind.get_direccio()

        for entrada in vector_entrades:
            if objectiu in entrada:
                color = colors[vector_entrades.index(entrada) % len(colors)]

                pygame.draw.circle(screen, color, (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2), cell_size[0]//8)
                pygame.draw.circle(screen, color, (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2), cell_size[0] // 8)

                arrow_start = (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2)
                arrow_end = (arrow_start[0] + dy * cell_size[0] // 2, arrow_start[1] + dx * cell_size[1] // 2)

                draw_arrow(screen, color, arrow_start, arrow_end, 12)

    # Actualitzar pantalla
    pygame.display.flip()
    clock.tick(3)  # Control de velocitat de la simulació (FPS)


# Dibuixa la fletxa que indica la direcció de cada individu
def draw_arrow(screen, color, start, end, arrow_head_size):
    dx = end[0] - start[0] #* 0.3
    dy = end[1] - start[1] #* 0.3
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

