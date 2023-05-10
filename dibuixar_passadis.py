import pygame
import sys
from pygame.locals import QUIT
import math

def dibuixar_passadis_pygame(n, m, passadis, individus):
    pygame.init()
    clock = pygame.time.Clock()

    # Obté el tamany de la pantalla del dispositiu on s'executi el programa
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Crea una finestra de pantalla completa
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    # Definim els colors
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
    parets.extend([(0, 0), (0, screen_width), (screen_height, 0), (screen_height, screen_width)])
    vector_entrades = passadis.get_entrades()
    entrades = [e for entrada in vector_entrades for e in entrada]
    obstacles = passadis.get_obstacles()

    for x, y in obstacles:
        pygame.draw.rect(screen, black, (int(y * screen_width / n), int(x * screen_height / m), int(screen_width / n), int(screen_height / m)))

    for x, y in parets:
        if (x, y) in passadis.get_parets():
            color = gray
        else:
            color = black

        pygame.draw.rect(screen, color, (int(y * screen_width / n), int(x * screen_height / m), int(screen_width / n), int(screen_height / m)))

        if (x, y) in entrades:
            for entrada in vector_entrades:
                if (x, y) in entrada:
                    color = colors[vector_entrades.index(entrada) % len(colors)]
            pygame.draw.circle(screen, color, (int(y * screen_width / n + screen_width / n // 2), int(x * screen_height / m + screen_height / m // 2)), int(min(screen_width / n, screen_height / m) // 4))

    # Dibuixar individus
    for ind in individus:
        if ind.posicio == None: continue

        objectiu = ind.get_objectiu()
        x, y = ind.get_posicio()
        dx, dy = ind.get_direccio()

        for entrada in vector_entrades:
            if objectiu in entrada:
                color = colors[vector_entrades.index(entrada) % len(colors)]

                pygame.draw.circle(screen, color, (int(y * screen_width / n + screen_width / n // 2), int(x * screen_height / m + screen_height / m // 2)), int(min(screen_width / n, screen_height / m) // 8))

                arrow_start = (int(y * screen_width / n + screen_width / n // 2), int(x * screen_height / m + screen_height / m // 2))
                arrow_end = (int((y + dy) * screen_width / n + screen_width / n // 2), int((x + dx) * screen_height / m + screen_height / m // 2))

                draw_arrow(screen, color, arrow_start, arrow_end, 12)

    # Actualitzar pantalla
    pygame.display.flip()
    clock.tick(2)  # Control de velocitat de la simulació (FPS)


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