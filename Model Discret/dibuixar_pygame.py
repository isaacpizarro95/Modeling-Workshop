import pygame
import sys
from pygame.locals import QUIT
import math

def dibuixar_passadis(passadis, screen, cell_size, clock, fps):
    """
    Dibuixa el passadís i els individus a la pantalla en un entorn de simulació pygame.

    Paràmentres:
    passadis (Passadis): L'objecte passadís que conté la configuració de la simulació.
    screen: La superfície de la pantalla de pygame en la qual es dibuixarà el passadís.
    cell_size (tuple): La mida de les cel·les del passadís en píxels.
    clock: L'objecte rellotge de pygame per controlar el temps de la simulació.
    fps (int): El nombre de fotogrames per segon desitjat per la simulació.
    """

    m = passadis.get_m()
    n = passadis.get_n()

    # Definim colors
    black = (0, 0, 0)  # Color negre
    white = (255, 255, 255)  # Color blanc
    gray = (128, 128, 128)  # Color gris
    
    # Llista de colors
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

    # Obté la llista de parets del passadís
    parets = passadis.get_parets()

    # Afegeix els extrems del passadís com a parets
    parets.extend([(0, 0), (0, n - 1), (m - 1, 0), (m - 1, n - 1)])

    # Obté els vectors de les entrades del passadís
    vector_entrades = passadis.get_entrades()

    # Obté les posicions dels vectors de les entrades del passadís
    entrades = [e for entrada in vector_entrades for e in entrada]

    # Obté els obstacles del passadís
    obstacles = passadis.get_obstacles()  

    # Dibuixa els obstacles
    for x, y in obstacles:
        pygame.draw.rect(screen, black, (y * cell_size[0], x * cell_size[1], cell_size[0], cell_size[1]))

    for x, y in parets:
        # Comprova si és una paret o una cantonada
        if (x, y) in passadis.get_parets():  
            color = gray
        else:
            color = black

        # Dibuixa les parets
        pygame.draw.rect(screen, color, (y * cell_size[0], x * cell_size[1], cell_size[0], cell_size[1]))

        # Comprova si és una entrada
        if (x, y) in entrades:  
            for entrada in vector_entrades:
                if (x, y) in entrada:
                    # Assigna un color a l'entrada
                    color = colors[vector_entrades.index(entrada) % len(colors)]

            # Dibuixa un cercle a l'entrada
            pygame.draw.circle(screen, color, (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2), cell_size[0] // 4)  

    # Dibuixar individus
    for ind in passadis.get_ind_in_passadis():
        objectiu = ind.get_objectiu()  # Obté l'objectiu de l'individu
        x, y = ind.get_posicio()  # Obté la posició de l'individu
        dx, dy = ind.get_direccio()  # Obté la direcció de l'individu

        for entrada in vector_entrades:
            if objectiu in entrada:
                # Assigna un color a l'objectiu
                color = colors[vector_entrades.index(entrada) % len(colors)]  

                # Dibuixa un cercle a l'objectiu
                pygame.draw.circle(screen, color, (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2), cell_size[0]//8)  

                # Punt d'inici de la fletxa
                arrow_inici = (y * cell_size[0] + cell_size[0] // 2, x * cell_size[1] + cell_size[1] // 2)

                # Punt final de la fletxa
                arrow_final = (arrow_inici[0] + dy * cell_size[0] // 2, arrow_inici[1] + dx * cell_size[1] // 2)  

                # Dibuixa una fletxa que indica la direcció de l'individu
                draw_arrow(screen, color, arrow_inici, arrow_final, 12)  

    # Actualitzar pantalla
    pygame.display.flip()

    # Control de velocitat de la simulació (FPS)
    clock.tick(fps)  


# Dibuixa la fletxa que indica la direcció de cada individu
def draw_arrow(screen, color, inici, final, arrow_head_size):
    """
    Dibuixa una fletxa que indica la direcció de l'individu a la pantalla en un entorn de simulació pygame.

    Paràmentres:
    screen: La superfície de la pantalla de pygame en la qual es dibuixarà la fletxa.
    color (tuple): El color de la fletxa en format RGB.
    inici (tuple): Les coordenades del punt d'inici de la fletxa (x, y).
    final (tuple): Les coordenades del punt final de la fletxa (x, y).
    arrow_head_size (int): La mida de la capçalera de la fletxa en píxels.
    """

    dx = final[0] - inici[0]  # Diferència en l'eix x
    dy = final[1] - inici[1]  # Diferència en l'eix y

    # Longitud del vector de direcció
    longitud = math.sqrt(dx * dx + dy * dy)  
    if longitud == 0:
        return
    
    udx = dx / longitud  # Component normalitzada en l'eix x
    udy = dy / longitud  # Component normalitzada en l'eix y

    # Angle de l'extrem de la fletxa
    arrow_head_angle = math.pi / 6

    # Punt de l'extrem de la fletxa
    arrow_tail = (final[0] - udx * arrow_head_size, final[1] - udy * arrow_head_size)


    arrow_left = (
        # Coordenada x de l'extrem esquerre de la fletxa
        arrow_tail[0] - udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        # Coordenada y de l'extrem esquerre de la fletxa
        arrow_tail[1] + udx * arrow_head_size * math.tan(arrow_head_angle / 2),  
    )  # Càlcul de les coordenades de l'extrem esquerre de la fletxa

    arrow_right = (
        # Coordenada x de l'extrem dret de la fletxa
        arrow_tail[0] + udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        # Coordenada y de l'extrem dret de la fletxa
        arrow_tail[1] - udx * arrow_head_size * math.tan(arrow_head_angle / 2),  
    )  # Càlcul de les coordenades de l'extrem dret de la fletxa

    # Dibuixa la línia des de l'inici fins a l'extrem de la fletxa
    pygame.draw.line(screen, color, inici, arrow_tail, 1)
    # Dibuixa el triangle de la fletxa
    pygame.draw.polygon(screen, color, [final, arrow_left, arrow_right])  