import numpy as np
import random

def calcul_sortida(entrada, passadis):
    """
    Calcula la sortida, que és un conjunt de posicions, a la que anirà l'individu.

    Paràmetres:
    entrada (tuple): Coordenades de l'entrada des de la qual parteix l'individu.
    passadis (Passadis): L'objecte passadís que conté la configuració del passadís.

    Retorna:
    tuple: Coordenades de la sortida cap a la qual s'ha de moure l'individu.
    """
    entrades = passadis.get_entrades()
    if entrada[0] == 0 or entrada[0] == (passadis.get_m()-1):
        # Excloure les sortides que estan a la mateixa fila que l'entrada
        posibles_sortides = [sortida for sortida in entrades if sortida[0][0] != entrada[0]]  
    else:
        #  Excloure les sortides que estan a la mateixa columna que l'entrada
        posibles_sortides = [sortida for sortida in entrades if sortida[0][1] != entrada[1]]  
    return random.choice(posibles_sortides)


def calcul_objectiu(posicio, sortida):
    """
    Calcula l'objectiu a partir de les posicions possibles de la sortida.

    Paràmetres:
    posicio (tuple): Coordenades de la posició actual de l'individu.
    sortida (list): Llista de tuples que contenen les posicions possibles de la sortida.

    Retorna:
    tuple: Coordenades de la posició exacta de la sortida cap al qual s'ha de moure l'individu (objectiu).
    """
    distancies = {}
    for pos in sortida:
        # Càlcul de la distància de Manhattan entre la posició actual i cada posició possible de la sortida
        distancies[np.sum(np.abs(np.array(pos) - np.array(posicio)))] = pos
    
    # Obtenció de la posició amb la menor distància a la posició actual (objectiu)
    objectiu = distancies[min([key for key in distancies.keys()])]  
    return objectiu


def calcul_direccio(seguent_pos, pos):
    """
    Calcula la direcció en la que es mourà l'individu.

    Paràmetres:
    seguent_pos (dupla): Coordenades de la posició següent a la que s'ha de moure l'individu
    pos (dupla): Coordenades de la posició actual de l'individu.

    Retorna:
    dupla: Coordenades de la direcció en la que es mourà l'individu.
    """

    # Calcula la diferencia en el eje x entre la posición siguiente y la posición actual
    direccio_x = seguent_pos[0] - pos[0]

    # Calacula la diferència en el eix y entre la posició següent i l'actual
    direccio_y = seguent_pos[1] - pos[1]
    return (direccio_x, direccio_y)


def calcul_distancia_direccio(individu, pos):
    """
    Calcula la distància entre les posicions a les que es mouria l'individu a partir de dos direccions diferents.

    Paràmetres:
    individu: L'objecte individu que conté la informació de l'individu
    pos (dupla): Coordenades de la posició a la que es vol calcular la distancia.

    Retorna:
    La distància entre les posicions considerant dos direccions diferents.
    """
    
    # Coordenades de la posició actual de l'individu
    x, y = individu.get_posicio()

    # Components de la direcció de l'individu
    dx, dy = individu.get_direccio()

    # Calcula la distància de Manhattan entre les posicions considerant dues direccions diferents
    distancia = np.sum(np.abs(np.array((x+dx, y+dy)) - np.array(pos)))
    return distancia


def calcul_camp_visio(individu, direccio):
    """
    Calcula el camp de visió de l'individu en funció de la direcció donada.

    Paràmetres:
    individu (objecte): L'objecte individu que conté la informació de l'individu.
    direccio (dupla): La direcció en què l'individu es mourà.

    Retorna:
    llista: Una llista de posicions que formen el camp de visió de l'individu.
    """
    # Obtenim les coordenades x i y de la posició actual de l'individu
    x, y = individu.get_posicio()

    # Obtenim les coordenades dx i dy de la direcció
    dx, dy = direccio

    # Calculem el signe de dx i de dy
    if dx != 0: signe_dx = int(dx / abs(dx))
    else: signe_dx = 0
    
    if dy != 0: signe_dy = int(dy / abs(dy))
    else: signe_dy = 0
    
    # Obtenim la mida del camp de visió de l'individu
    n = individu.get_camp_visio()

    # Creem una llista buida per emmagatzemar les posicions del camp de visió
    posicions_visio = []

    # Comprovem si la direcció no és zero en x i en y
    if dx != 0 and dy != 0:

        # Bucle per generar les posicions del camp de visió en funció de n
        for i in range(n):
            for j in range(n):
                # Afegim la posició (x + signe_dx * i + dx, y + signe_dy * j + dy) a la llista de posicions del camp de visió
                posicions_visio.append((x + dx + signe_dx * i, y + dy + signe_dy * j))

    # Comprovem si la direcció no és zero en x
    elif dx != 0:
        
        # Bucle per generar les posicions del camp de visió en funció de n
        for i in range(1, n + 1):
            for j in range(1 - i, i):
                # Afegim la posició (x + signe_dx * i, y + j) a la llista de posicions del camp de visió
                posicions_visio.append((x + signe_dx * i, y + j))
                
    # Comprovem si la direcció no és zero en y
    elif dy != 0:
        
        # Bucle per generar les posicions del camp de visió en funció de n
        for i in range(1, n + 1):
            for j in range(1 - i, i):
                # Afegim la posició (x + j, y + signe_dy * i) a la llista de posicions del camp de visió
                posicions_visio.append((x + j, y + signe_dy * i))

    # Retornem la llista de posicions que formen el camp de visió de l'individu
    return posicions_visio


def consultar_interaccio(ind_a_objectiu, ind_a_direccio, pos, passadis):
    """
    Consulta l'interacció entre dos individus en una determinada posició.

    Paràmetres:
    ind_a_objectiu (dupla): Coordenades de l'objectiu de l'individu A.
    ind_a_direccio (dupla): Direcció de l'individu A.
    pos (dupla): Coordenades de la posició a consultar l'interacció (posició de l'individu B)
    passadis: L'objecte passadís que conté la configuració del passadís.

    Retorna:
    int: 1 si l'interacció implica un moviment en grup, 0 si és una col·lisió, -1 si no hi ha interacció.
    """
    # Obtenim l'individu que hi ha en aquella posició
    ind_b = passadis.diccionario_posicion.get(pos, None)  

    if ind_b is not None:
        ind_b_direccio = ind_b.get_direccio()
        ind_b_objectiu = ind_b.get_objectiu()

        if ind_b_direccio[0] != 0 and ind_a_direccio[0] != 0:

            # Si els individus van en la mateixa direcció
            if ind_b_direccio[0] - ind_a_direccio[0] == 0 and ((ind_a_objectiu[0] == ind_b_objectiu[0]) or (ind_a_objectiu[1] == ind_b_objectiu[1])):
                return 1
            else:
                # Si els individus no van en la mateixa direcció
                return 0  

        elif ind_b_direccio[0] == 0 or ind_a_direccio[0] == 0:
            # Si els individus van en la mateixa direcció
            if ind_b_direccio[1] - ind_a_direccio[1] == 0 and ((ind_a_objectiu[0] == ind_b_objectiu[0]) or (ind_a_objectiu[1] == ind_b_objectiu[1])):
                return 1
            else:
                # Si els individus no van en la mateixa direcció
                return 0  

    else:
        # Si no hi ha interacció
        return -1


def moure_individu(individu, passadis):
    """
    Mou un individu en el passadís segons una lògica de moviment.

    Paràmetres:
    individu: L'objecte individu que es vol moure.
    passadis: L'objecte passadís que conté la configuració del passadís.    

    Retorna: None
    """ 

    # Acualitzem el temps que porta fent el recorregut l'individu
    #individu.trajecte.add_t_recorregut()
    individu.trajecte.add_t_recorregut()

    # Fem tants moviments com indiqui la velocitat (en aquest model la velocitat només pot ser entera)
    for i in range(individu.get_velocitat()):
        # Obtenim les coordenades x i y de la posició actual de l'individu
        x, y = individu.get_posicio()

        # Calculem l'objectiu de l'individu
        objectiu = calcul_objectiu((x,y), individu.get_sortida())

        # Establim l'objectiu de l'individu
        individu.set_objectiu(objectiu)  

        # Obtenim la matriu del passadís
        matriu = passadis.get_passadis()  

        # Eliminem la posició anterior de l'individu al diccionari de posicions
        passadis.diccionario_posicion.pop((x, y), None)  

        # Comprovem si l'individu ha arribat a l'objectiu
        if (x, y) == objectiu:
            # Establim la posició de l'individu com a None
            individu.set_posicio(None)

            # Eliminem l'individu de la llista d'individus en el passadís
            passadis.ind_in_passadis.remove(individu)  
            return 

        posicions = []

        # Obtenim les posicions vàlides adjacents a la posició actual en funció de l'objectiu
        if objectiu[0] != 0:
            posicions = [(x, y), (x+1, y), (x, y-1), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y-1), (x-1, y+1)]
            #posicions = [(x+1, y), (x, y-1), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y-1), (x-1, y+1)]
        else:
            posicions = [(x, y), (x-1, y), (x, y-1), (x, y+1), (x-1, y+1), (x-1, y-1), (x+1, y+1), (x+1, y-1)]
            #posicions = [(x-1, y), (x, y-1), (x, y+1), (x-1, y+1), (x-1, y-1), (x+1, y+1), (x+1, y-1)]

        # Analitzem les posicions vàlides
        puntuacions = {}
        for pos in posicions:
            # Les posicions vàlides son aquelles on no hi han obstacles o parets
            if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 4:
                # Si en una de les posicions adjacents hi ha un individu comprovem quina interacció 
                # s'esta tenint
                if matriu[pos] == 1:
                    # Si aquest individu va en una direcció similar a la del nostre individu 
                    # considerem que és un moviment agrupat (en carril)
                    if consultar_interaccio(objectiu, individu.get_direccio(), pos, passadis) == 1:
                        individu.trajecte.add_agrupat()

                    # Si aquest individu va en una direcció contraria a la del nostre individu 
                    # considerem que és una col·lisió
                    elif consultar_interaccio(objectiu, individu.get_direccio(), pos, passadis) == 0: 
                        individu.trajecte.add_colisio()
                
                else: 
                    # Calculem la distancia a l'objectiu
                    distancia_objectiu = np.sum(np.abs(np.array(pos) - np.array(objectiu)))

                    # Calculem la quantitat de canvi que fem en la direccio
                    canvi_direccio = calcul_distancia_direccio(individu, pos)
                    individu.trajecte.add_canvi_direccio(canvi_direccio)

                    # Direcció respecte la nova possible posició
                    nova_direccio = (pos[0] - x, pos[1] - y)

                    # Camp de visió en el sentit de la nova direcció
                    camp_visio = calcul_camp_visio(individu, nova_direccio)

                    # Analitzem si fer aquest moviment implica agruparnos o aproparnos a col·lisions
                    colisions = 0
                    inds_agrupats = 0
                    for cv_pos in camp_visio:
                        if 0 <= cv_pos[0] < passadis.get_m() and 0 <= cv_pos[1] < passadis.get_n() and matriu[cv_pos] == 1:         
                            if consultar_interaccio(objectiu, nova_direccio, cv_pos, passadis) == 1: 
                                inds_agrupats += 1
                            else: 
                                colisions += 1                    

                    # Obtenim els coeficients d'importància relatius a cada variable
                    p_agrupats, p_colisions, p_distancia, p_canvi = individu.trajecte.get_ponderacions()

                    # Calculem la puntuació corresponent a aquesta posició
                    puntuacio = inds_agrupats * p_agrupats - colisions * p_colisions - distancia_objectiu * p_distancia - canvi_direccio * p_canvi
                    
                    puntuacions[puntuacio] = pos

        # Si no hi ha posicions vàlides disponibles no movem a l'individu i finalitzem la funció
        if not puntuacions: return

        # Seleccionem la posició amb la puntuació més alta
        posicio_escollida = puntuacions[max([key for key in puntuacions.keys()])]

        # Calculem la direcció de l'individu (és equivalent a calcular quin és el moviment que ha fet)
        individu.set_direccio(calcul_direccio(posicio_escollida, (x,y)))

        # Si la posició escollida coincideix amb l'objectiu, l'individu finalitza el trajecte
        # i eliminem la seva posició
        if posicio_escollida in passadis.get_entrades() and individu.get_objectiu() == posicio_escollida:
            individu.set_posicio(posicio_escollida)
            individu.set_posicio(None)
            matriu[x, y] = 0
            passadis.ind_in_passadis.remove(individu)  

        # Si encara no ha arribat a l'objectiu simplement actualitzem la posició
        else:
            # Deixem buida la posició on estava abans l'individu
            matriu[x, y] = 0

            # Ocupem la nova posició
            matriu[posicio_escollida] = 1

            # Actualitzem la posició en l'objecte individu
            individu.set_posicio(posicio_escollida)

            # Actualitzem el diccionari de posicions del passadís
            passadis.diccionario_posicion[individu.posicio] = individu
