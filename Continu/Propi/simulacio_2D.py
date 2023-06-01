import random
import config_individus as ci
import config_passadis as cp
import dibuixar_passadis as dp
import utils_individus as ui
import pygame
import numpy as np
import moviment as mov
import matplotlib.pyplot as plt
import seaborn as sns

def simulacio_2D(passadis, num_iteracions, aforament, fps):
    m = passadis.get_m()
    n = passadis.get_n()
    entrades = passadis.get_entrades()  # Obtenim les entrades/sortides del passadís

    # Inicializar Pygame
    pygame.init()

    # Obtener el tamaño de la pantalla del dispositivo
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w * 0.5
    screen_height = screen_info.current_h * 0.9

    # Calcular el factor de escala
    scale_x = screen_width / m
    scale_y = screen_height / n

    # Crear la ventana
    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))

    # Crear un reloj para controlar la velocidad de actualización de la pantalla
    clock = pygame.time.Clock()

    # Parametres dels individus
    id_individu = 0 
    v_min = 0.02
    v_max = 0.2
    radi = 0.3
    temps_horitzo = 4
    delta = n/20

    # Comptem i classifiquem les interaccions entre els individus
    colisions = 0
    interaccions = 0

    # Simulem el moviment dels individus a cada interació
    individus = []
    velocitats = {}

    for t in range(num_iteracions):
        if t % 2 == 0:
            # Creem un nombre aleatori d'individus que anirá de 0 al màxim que ens permeti l'aforament' tenint en compte els individus que ja hi han 
            nous_individus = random.randint(0, (aforament-len(passadis.ind_in_passadis))//10)
            if nous_individus > int(m/(2*radi)) - 1: nous_individus = int(m/(2 * radi)) - 1

            # Dividim les entrades segons el radi dels individus
            posicions_entrades = ui.calcul_posicions_entrada(m, n, radi, delta)

            # Afegim els individus nous que apareixen a les entrades i els afegim a la llista
            for j in range(1, nous_individus + 1):
                # if len(passadis.ind_in_passadis) >= aforament - 2: break
                # for k in range(2):
                # Calculem el id del nou individu
                id_individu += 1

                # Calculem l'entrada de l'individu
                index_entrada = random.randrange(len(posicions_entrades))
                entrada = posicions_entrades[index_entrada]
                posicions_entrades.pop(index_entrada)
                
                # Calculem la sortida i l'objectiu
                sortida = ui.calcul_sortida(entrada, entrades)
                objectiu = ui.calcul_objectiu(sortida)

                # Classifiquem a l'individu segons el seu objectiu
                if objectiu[1] == delta: grup = 0
                else: grup = 1

                # Calculem la velocitat preferida
                velocitat = ui.calcul_velocitat_inicial(v_min, v_max)

                # Creem el nou individu amb els paràmetres i variables calculats previament
                individu = ci.Individu(id_individu, entrada, sortida, objectiu, grup, v_min, v_max, velocitat, m, n, radi, temps_horitzo)
                
                # Afegim a l'individu a la llista total, a l'aforament del passadís
                individus.append(individu)
                passadis.ind_in_passadis.append(individu)
                passadis.ind_posicions[individu] = entrada
                velocitats[individu] = []
        
        for ind in passadis.get_ind_in_passadis():
            mov.calcul_nova_velocitat(ind, passadis.get_ind_in_passadis())
            mov.actualitzar_posicio(ind, passadis)
            velocitats[ind].append(ind.get_velocitat())

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Quantitat invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dp.dibuixar_passadis_pygame(n, m, passadis, individus, scale_x, scale_y, screen, clock, fps)

        
    #recorreguts = []
    datos = []
    colisions = 0
    moviments = 0
    for ind in individus:
        print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha tingut velocitat mitja: {np.average(velocitats[ind])}\n")
        #print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha fet el recorregut:\n{ind.get_recorregut()}\n")
        moviments += len(ind.get_recorregut())
        datos.append(abs(np.average(velocitats[ind])))
        colisions += ind.get_colisions()
    #print(f"Hi han hagut {colisions} col·lisions en un total de {moviments} moviments en {t+1} segons en un mapa {m} * {n} de {aforament} individus on hi han circulat {len(individus)} individus en total\n")
    # print(f"Per tant de mitja hi han hagut {colisions/len(individus):.2f} col·lisions i {interaccions/len(individus):.2f} interaccions de mitja per individu\n")
    # Crear el gráfico de densidad
    
    # sns.kdeplot(datos, shade=True)

    # # Configurar el título y etiquetas de los ejes
    # plt.title('Distribución de números reales')
    # plt.xlabel('Valores')
    # plt.ylabel('Densidad')

    # # Mostrar el gráfico
    # plt.show()