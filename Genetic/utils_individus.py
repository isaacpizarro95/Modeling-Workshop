import numpy as np
import random

# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(entrada, passadis):
    entrades = passadis.get_entrades()
    if entrada[0] == 0 or entrada[0] == (passadis.get_m()-1): 
        posibles_sortides = [sortida for sortida in entrades if sortida[0][0] != entrada[0]]
    else:
        posibles_sortides = [sortida for sortida in entrades if sortida[0][1] != entrada[1]]
    return random.choice(posibles_sortides)


# Calcula l'objectiu dins de les posicions possibles de la sortida
def calcul_objectiu(posicio, sortida):
    distancies = {}
    for pos in sortida:
        distancies[np.linalg.norm(np.array(pos) - np.array(posicio))] = pos
    
    objectiu = distancies[min([key for key in distancies.keys()])]
    return objectiu


# Calcula la velocitat màxima que podrà tenir un individu
def calcul_velocitat():
    velocitats = [1, 2, 3]
    probabilitats = [0.35, 0.4, 0.25]

    # La funció np.random.choice pren com a argument la llista de valors possibles (velocitats) i la distribució discreta de probabilitats 
    # corresponent (probabilitats). L'argument p indica les probabilitats corresponents a cada valor de la llista.
    velocitat = np.random.choice(velocitats, p=probabilitats)
    return velocitat


# Calcula la direcció de l'individu
def calcul_direccio(seguent_pos, pos):
    direccio_x = seguent_pos[0] - pos[0]
    direccio_y = seguent_pos[1] - pos[1]
    return ((direccio_x, direccio_y))


# Calcula la distancia entre les posicions a les que mourien dos direccions diferents
def calcul_distancia_direccio(individu, pos):
    x, y = individu.get_posicio()
    dx, dy = individu.get_direccio()

    distancia = np.linalg.norm(np.array((x+dx, y+dy)) - np.array(pos))
    return distancia


# Crea un camp de visio per a l'individu a partir de n. S'utilitza cada vegada que l'individu es mou
def calcul_camp_visio(individu, direccio):
    x, y = individu.get_posicio()
    dx, dy = direccio
    n = individu.get_camp_visio()
    posicions_visio = []

    if dx != 0 and dy != 0:
        signe_dx = int(dx / abs(dx))
        signe_dy = int(dy / abs(dy))
        for i in range(n):
            for j in range(n):
                posicions_visio.append((x + signe_dx * i + dx, y + signe_dy * j + dy))

    elif dx != 0:
        signe_dx = int(dx / abs(dx))
        for i in range(1, n + 1):
            for j in range(1 - i, i):
                posicions_visio.append((x + signe_dx * i, y + j))
                
    elif dy != 0:
        signe_dy = int(dy / abs(dy))
        for i in range(1, n + 1):
            for j in range(1 - i, i):
                posicions_visio.append((x + j, y + signe_dy * i))

    return posicions_visio

# Torna 1 si la interacció amb l'altre individu comporta un moviment en grup o 0 si és una col·lissió
def consultar_interaccio(ind_a_objectiu, ind_a_direccio, pos, passadis):
    ind_b = passadis.diccionario_posicion.get(pos, None) # Obtenim el individu que hi ha en aquella posició
    
    if ind_b is not None:
        ind_b_direccio = ind_b.get_direccio()
        ind_b_objectiu = ind_b.get_objectiu()
        if ind_b_direccio[0] != 0 and ind_a_direccio[0] != 0:
            # Si els individus van en la mateixa direcció
            if ind_b_direccio[0] - ind_a_direccio[0] == 0 and ((ind_a_objectiu[0] == ind_b_objectiu[0]) or (ind_a_objectiu[1] == ind_b_objectiu[1])):
                return 1
            else: return 0 # Si els individus no van en la mateixa direcció
    
        elif ind_b_direccio[0] == 0 or ind_a_direccio[0] == 0:
            # Si els individus van en la mateixa direcció
            if ind_b_direccio[1] - ind_a_direccio[1] == 0 and ((ind_a_objectiu[0] == ind_b_objectiu[0]) or (ind_a_objectiu[1] == ind_b_objectiu[1])):
                return 1
            else: return 0 # Si els individus no van en la mateixa direcció

    else: return -1

# tipus_interaccio == 1 si la interacció es un moviment agrupat i tipus_interaccio == 0 si es la interacció és una col·lissió
def anotar_interaccio(ind, tipus_interaccio):
    if tipus_interaccio == 1: ind.trajecte.add_agrupat()
    elif tipus_interaccio == 0: ind.trajecte.add_colisio()


                    # *********** FALTA FER *********** #

# EL QUE TRANSMITIM DE GENERACIÓ EN GENERACIÓ SERAN ELS PESOS QUE S'ASSIGNEN A CADA VARIABLE PER FER LA SUMA.
# PROCÉS DE L'ALGORITME GENETIC: CREACIÓ GENERACIÓ, SELECCIÓ, DESCENDENCIA, MUTACIÓ, FUNCIÓ APTITUD

                    # *********** FALTA FER *********** #

def moure_individu(individu, passadis):
    individu.trajecte.add_t_recorregut()
    for i in range(individu.get_velocitat()):
        x, y = individu.get_posicio()
        objectiu = calcul_objectiu((x,y), individu.get_sortida())
        individu.set_objectiu(objectiu)

        matriu = passadis.get_passadis()
        passadis.diccionario_posicion.pop((x, y), None) # Eliminem la posició anterior de l'individu al diccionari

        if((x,y) == objectiu):
            individu.set_posicio(None)
            passadis.ind_in_passadis.remove(individu)
            return
        
        # Obtenim les posicions vàlides adjacents a la posició actual
        posicions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1)]
        puntuacions = {}

        for pos in posicions:
            if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 4:
                if matriu[pos] == 1: 
                    anotar_interaccio(individu, consultar_interaccio(objectiu, individu.get_direccio(), pos, passadis))
                
                else: 
                    # Calculem la distancia a l'objectiu
                    distancia_objectiu = np.linalg.norm(np.array(pos) - np.array(objectiu))

                    # Calculem la quantitat de canvi que fem en la direccio
                    canvi_direccio = calcul_distancia_direccio(individu, pos)

                    # Verifiquem si fer aquest moviment implica agruparnos o aproparnos a col·lisions
                    colisions = 0
                    inds_agrupats = 0
                    nova_direccio = (pos[0] - x, pos[1] - y) # Direcció respecte la nova possible posició
                    camp_visio = calcul_camp_visio(individu, nova_direccio) # Camp de visió en el sentit de la nova direcció
                    for cv_pos in camp_visio:
                        if 0 <= cv_pos[0] < passadis.get_m() and 0 <= cv_pos[1] < passadis.get_n() and matriu[cv_pos] == 1:         
                            if consultar_interaccio(objectiu, nova_direccio, cv_pos, passadis) == 1: inds_agrupats += 1
                            else: colisions += 1                    

                    # Aqui s'afegeixen els pesos relatius a cada variable
                    p_agrupats, p_colisions, p_distancia, p_canvi = individu.trajecte.get_ponderacions()

                    # Ara podem calcular la puntuació corresponent a aquesta posició
                    puntuacio = inds_agrupats * p_agrupats - colisions * p_colisions - distancia_objectiu * p_distancia - canvi_direccio * p_canvi
                    puntuacions[puntuacio] = pos

        if not puntuacions: return

        # Seleccionem la posició amb la distància més curta a l'objectiu
        posicio_escollida = puntuacions[max([key for key in puntuacions.keys()])]

        # Calculem la direcció de l'individu (és equivalent a calcular quin és el moviment que ha fet)
        individu.set_direccio(calcul_direccio(posicio_escollida, (x,y)))

        # Si la direcció escollida és una entrada/sortida, l'individu arriba al seu objectiu i eliminem la seva posició
        if posicio_escollida in passadis.get_entrades() and individu.get_objectiu() == posicio_escollida:
            individu.set_posicio(posicio_escollida)
            matriu[x, y] = 0
        else:
            # Actualitzem la posició de l'individu i la matriu
            matriu[x, y] = 0
            matriu[posicio_escollida] = 1
            individu.set_posicio(posicio_escollida)
            passadis.diccionario_posicion[individu.posicio] = individu
