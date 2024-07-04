import random
import config_individus as ci
import config_passadis as cp
import dibuixar_passadis as dp
import utils_individus as ui
import pygame
import numpy as np
import moviment as mov
# import matplotlib.pyplot as plt
# import seaborn as sns
import time

def simulacio(passadis, num_iteracions, aforament, escalat_pixel, fps):
    """
    Simula el moviment d'individus en un passadís 2D per un nombre determinat d'iteracions.

    Paràmetres:
    passadis: Objecte Passadis que conté la informació del passadís i els individus dins.
    num_iteracions: Nombre d'iteracions de la simulació.
    aforament: Nombre màxim d'individus que pot haver-hi al passadís.
    escalat_pixel: Unitat de tamany base dels píxels de la simulació
    fps: Enter que indica el nombre de frames per segon que es volen en la simulació.

    La funció gestiona tota la simulació: crea els individus, els mou i els dibuixa.
    """

    # Obtenim les dimensions i les entrades del passadís
    m = passadis.get_m()
    n = passadis.get_n()
    entrades = passadis.get_entrades()

    # Iniciem Pygame
    pygame.init()

    # Obtenim les dimensions de la pantalla del dispositiu
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Calculem les dimensions de la finestra de la simulació
    screen_width = m * escalat_pixel
    screen_height = n * escalat_pixel

    # Creem la finestra de la simulació
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Calculem els factors d'escala per a les dimensions x i y
    scale_x = screen_width / m
    scale_y = screen_height / n

    # Creem un rellotge per controlar la velocitat d'actualització de la pantalla
    clock = pygame.time.Clock()

    # Definim els paràmetres dels individus
    id_individu = 0 
    v_min = 0.02
    v_max = 0.2
    radi = 0.3
    temps_horitzo = 3
    delta = n/20

    # Inicialitzem les llistes per als individus i les seves velocitats
    individus = []
    velocitats = {}

    # Iniciem la simulació
    for t in range(num_iteracions):
        if t % 2 == 0:
            # Calculem el nombre d'individus nous a afegir
            nous_individus = random.randint(0, (aforament-len(passadis.ind_in_passadis))//10)
            if nous_individus > int(m/(2*radi)) - 1: nous_individus = int(m/(2 * radi)) - 1

            # Calculem les possibles posicions d'entrada
            posicions_entrades = ui.calcul_posicions_entrada(m, n, radi, delta)

            # Creem els nous individus i els afegim a les llistes corresponents
            for j in range(1, nous_individus + 1):
                # Calculem l'id del nou individu
                id_individu += 1

                # Calculem l'entrada de l'individu
                index_entrada = random.randrange(len(posicions_entrades))
                entrada = posicions_entrades[index_entrada]

                # Eliminem aquesta entrada de les possibles entrades per a no posar dos 
                # individus en la mateixa entrada al mateix temps
                posicions_entrades.pop(index_entrada)

                # Calculem la sortida i l'objectiu de l'individu
                sortida = ui.calcul_sortida(entrada, entrades)
                objectiu = ui.calcul_objectiu(sortida)

                # Classifiquem a l'individu segons el seu objectiu
                if objectiu[1] == delta: grup = 0
                else: grup = 1

                # Calculem la velocitat preferida de l'individu
                velocitat = ui.calcul_velocitat_inicial(v_min, v_max)

                # Creem el nou individu
                individu = ci.Individu(id_individu, entrada, sortida, objectiu, grup, v_min, v_max, velocitat, m, n, radi, temps_horitzo)

                # Afegim l'individu a les llistes corresponents
                individus.append(individu)
                passadis.ind_in_passadis.append(individu)
                passadis.ind_posicions[individu] = entrada
                velocitats[individu] = []

        # Aquest bucle gestiona el moviment dels individus
        # Actualitzem la velocitat i la posició de cada individu en el passadís
        for ind in passadis.get_ind_in_passadis():
            mov.calcul_nova_velocitat(ind, passadis.get_ind_in_passadis())
            mov.actualitzar_posicio(ind, passadis)
            velocitats[ind].append(ind.get_velocitat())

        # Mostrem el nombre d'individus en el passadís i en total en cada iteració
        print(f"Quantitat invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada iteració
        dp.dibuixar_passadis(passadis, scale_x, scale_y, screen, clock, fps)



#     #recorreguts = []
#     datos = []
#     colisions = 0
#     moviments = 0
#     for ind in individus:
#         print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha tingut velocitat mitja: {np.average(velocitats[ind])}\n")
#         #print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha fet el recorregut:\n{ind.get_recorregut()}\n")
#         moviments += len(ind.get_recorregut())
#         datos.append(abs(np.average(velocitats[ind])))
#         colisions += ind.get_colisions()
#     #print(f"Hi han hagut {colisions} col·lisions en un total de {moviments} moviments en {t+1} segons en un mapa {m} * {n} de {aforament} individus on hi han circulat {len(individus)} individus en total\n")
#     # print(f"Per tant de mitja hi han hagut {colisions/len(individus):.2f} col·lisions i {interaccions/len(individus):.2f} interaccions de mitja per individu\n")
#     # Crear el gráfico de densidad
    
#     # sns.kdeplot(datos, shade=True)

#     # # Configurar el título y etiquetas de los ejes
#     # plt.title('Distribución de números reales')
#     # plt.xlabel('Valores')
#     # plt.ylabel('Densidad')

#     # # Mostrar el gráfico
#     # plt.show()