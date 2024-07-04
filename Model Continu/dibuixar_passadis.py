import pygame
import sys
from pygame.locals import QUIT
import numpy as np
import math
import config_individus as ci
import utils_individus as ui

def dibuixar_passadis(passadis, scale_x, scale_y, screen, clock, fps):
    """
    Dibuixa un passadís i els individus que hi ha dins en una pantalla de pygame.

    Paràmetres:
    passadis: Objecte Passadis que conté la informació del passadís i els individus dins.
    scale_x, scale_y: Factors d'escala per a les coordenades x i y, respectivament. 
    Aquests s'utilitzen per ajustar les dimensions del passadís a la pantalla de pygame.
    
    screen: La superfície de la pantalla de pygame on es dibuixarà el passadís.
    clock: Objecte Clock de pygame que s'utilitza per controlar la velocitat de la simulació.
    fps: Enter que indica el nombre de frames per segon que es volen en la simulació.

    Aquesta funció dibuixa el passadís, les entrades i els individus a la pantalla de pygame. 
    Cada individu es dibuixa com un cercle amb un color que correspon a la seva entrada. 
    També es dibuixa una fletxa que indica la direcció de cada individu. La funció també gestiona els 
    esdeveniments de sortida, com ara tancar la finestra o prémer la tecla ESC.
    """

    # Dimensions del passadís
    m = passadis.get_m()
    n = passadis.get_n()

    # Definim colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    color_entrada1 = (0, 0, 255)  # Blau
    color_entrada2 = (255, 0, 0)  # Vermell

    # Asociar cada entrada amb un dels colors
    entrades = passadis.get_entrades()
    entrades_colors = {tuple(entrades[0]): color_entrada1, tuple(entrades[1]): color_entrada2}

    # individu1 = ci.Individu(0, (8,12), ui.calcul_sortida((8,1.25), entrades), (8, 24), 1, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu2 = ci.Individu(1, (10.2,18), ui.calcul_sortida((6,1.25), entrades), (3, 24), 1, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu3 = ci.Individu(2, (13.9,20), ui.calcul_sortida((4,1.25), entrades), (4, 24), 1, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu4 = ci.Individu(3, (12.1,17), ui.calcul_sortida((2,1.25), entrades), (5, 24), 1, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu5 = ci.Individu(4, (11.3, 15.5), ui.calcul_sortida((10,1.25), entrades), (6, 24), 1, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu6 = ci.Individu(5, (5,11.8), ui.calcul_sortida((4,23.5), entrades), (2, 1), 0, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu7 = ci.Individu(6, (4,14.2), ui.calcul_sortida((6,23.5), entrades), (3, 1), 0, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # individu8 = ci.Individu(7, (6,13.5), ui.calcul_sortida((8,23.5), entrades), (4, 1), 0, 0.02, 0.2, ui.calcul_velocitat_inicial(0.02, 0.2), 15, 25, 0.5, 3)
    # #individus = [individu1, individu2, individu3, individu4, individu5, individu6, individu7, individu8]
    # individus = [individu1]

    # inds_agrupats = [individu2.get_posicio(), individu3.get_posicio(), individu4.get_posicio(), individu5.get_posicio()]
    # inds_colisions = [individu6.get_posicio(), individu7.get_posicio(), individu8.get_posicio()]

    # dists_agrupats = []
    # for pos in inds_agrupats:
    #     dist = np.linalg.norm(np.array(individu1.get_posicio()) - pos)
    #     dists_agrupats.append(dist)

    # dists_colisions = []
    # for pos in inds_colisions:
    #     dist = np.linalg.norm(np.array(individu1.get_posicio()) - pos) 
    #     dists_colisions.append(dist)

    # if inds_agrupats:
    #     # Calculem els inversos de les distàncies als individus agrupats
    #     pesos_agr = np.reciprocal(dists_agrupats)
    #     pesos_agr = np.where(pesos_agr == np.inf, 1e10, pesos_agr)

    #     # Mitjana ponderada utilitzant els inversos de les distàncies i les posicions ajustades dels individus agrupats
    #     mitja_agrupats = np.average(np.array(inds_agrupats), axis=0, weights=pesos_agr) 
    # else:
    #     mitja_agrupats = pos

    # if inds_colisions:
    #     # Calculem els inversos de les distàncies als individus amb potencial col·lisió
    #     pesos_col = np.reciprocal(dists_colisions)
    #     pesos_col = np.where(pesos_col == np.inf, 1e10, pesos_col)
    #     # Mitjana ponderada utilitzant els inversos de les distàncies i les posicions ajustades dels individus amb potencial col·lisió
    #     mitja_colisions = np.average(np.array(inds_colisions), axis=0, weights=pesos_col)
    # else:
    #     mitja_colisions = pos
    # objectiu = (8, 23.5)
    # pos = np.array((8,12))
    # nova_direccio = 0.05 * (objectiu - pos) + 0.5 * (mitja_agrupats - pos) - 0.4 * (mitja_colisions - pos)
    # nova_direccio_norm = nova_direccio / np.linalg.norm(nova_direccio)
    # nova_velocitat = 0.2 * nova_direccio_norm
    # nova_posicio = pos + np.array(nova_velocitat)
    # individu1.set_velocitat(nova_velocitat)
    # individu1.set_posicio(nova_posicio)

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
    
    #for individu in passadis.get_ind_in_passadis():
    for individu in passadis.get_ind_in_passadis():
        pos = individu.get_posicio()
        
        # El individuo ha salido del mapa
        if pos is None:  continue
        # Obtener el color de la salida de este individuo
        color_individu = entrades_colors[tuple(individu.get_sortida())]
        
        # Obtener la posición del individuo y aplicar el factor de escala
        pos = (int(pos[0]*scale_x), int(pos[1]*scale_y))

        # Dibuja el punt de la posició en la que està l'individu
        pygame.draw.circle(screen, color_individu, pos, 1)  
        
        # Dibuja la circunferencia
        # radius = individu.get_radi() * min(scale_x, scale_y)
        # pygame.draw.circle(screen, color_individu, pos, radius, 1)  

        # Obtenim la velocitat per poder dibuixar la direcció que porta l'individu
        velocitat = individu.get_velocitat()

        if np.linalg.norm(velocitat) != 0:
            # Normalitzar la velocitat per obtindre la direcció
            direccion = velocitat / np.linalg.norm(velocitat)

            # Escalar la direcció per a que la fletxa tingui un tamany constant
            direccion *= 15

            # Calcular els punts per al triangle de la fletxa
            punta = tuple(pos + direccion)

            # Dibuixa una fletxa que indica la direcció de l'individu
            draw_arrow(screen, color_individu, pos, punta, 10)  
    
    # Actualitzar pantalla
    pygame.display.flip()

    # Control de velocitat de la simulació (FPS)
    clock.tick(fps)  


# Dibuixa la fletxa que indica la direcció de cada individu
def draw_arrow(screen, color, start, end, arrow_head_size):    
    """
    Dibuixa una fletxa que indica la direcció de l'individu a la pantalla en un entorn de simulació pygame.

    Paràmentres:
    screen: La superfície de la pantalla de pygame en la qual es dibuixarà la fletxa.
    color (tupla): El color de la fletxa en format RGB.
    start (dupla): Les coordenades del punt d'inici de la fletxa (x, y).
    end (dupla): Les coordenades del punt final de la fletxa (x, y).
    arrow_head_size (int): La mida de la capçalera de la fletxa en píxels.
    """

    # Diferència en l'eix x
    dx = int(end[0] - start[0])

    # Diferència en l'eix y
    dy = int(end[1] - start[1])

    # Longitud del vector de direcció
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return
    
    # Component normalitzada en l'eix x
    udx = dx / length
    # Component normalitzada en l'eix y
    udy = dy / length

    # Angle de l'extrem de la fletxa
    arrow_head_angle = math.pi / 6

    # Punt de l'extrem de la fletxa
    arrow_tail = (end[0] - udx * arrow_head_size, end[1] - udy * arrow_head_size)

    # Càlcul de les coordenades de l'extrem esquerre de la fletxa
    arrow_left = (
        # Coordenada x de l'extrem esquerre de la fletxa
        arrow_tail[0] - udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        # Coordenada y de l'extrem esquerre de la fletxa
        arrow_tail[1] + udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    # Càlcul de les coordenades de l'extrem dret de la fletxa
    arrow_right = (
        # Coordenada x de l'extrem dret de la fletxa
        arrow_tail[0] + udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        # Coordenada y de l'extrem dret de la fletxa
        arrow_tail[1] - udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    # Dibuixa la línia des de l'inici fins a l'extrem de la fletxa
    pygame.draw.line(screen, color, start, arrow_tail, 1)

    # Dibuixa el triangle de la fletxa
    pygame.draw.polygon(screen, color, [end, arrow_left, arrow_right])