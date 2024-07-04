import random
import classe_individus as ci
import utils_individus as ui
import dibuixar_pygame as dpygame
import pygame
import matplotlib.pyplot as plt
import time
import numpy as np
import classe_passadis as cp


def generar_ponderacions(n):
    """
    Genera un vector de ponderacions aleatòries.

    Args:
        n (int): Nombre de ponderacions a generar.

    Returns:
        list: Vector de ponderacions generades.
    """

    # Generar n-1 números aleatoris entre 0.1 i 0.7
    ponderacions = [round(random.uniform(0.1, 0.7), 2) for _ in range(n-1)]
    
    # Calcular la suma total de les ponderacions generades
    total = sum(ponderacions)

    # Normalitzar les ponderacions perquè sumin 0.9 (es deixa un espai per a la quarta ponderació)
    ponderacions = [round(i / total * 0.9, 2) for i in ponderacions]

    # Corregir possibles errors d'arrodoniment
    diferencia = 0.9 - sum(ponderacions)
    if diferencia != 0:
        # Si la primera ponderació més la diferència és major que 0.7, afegim la diferència a la ponderació més petita
        if ponderacions[0] + diferencia > 0.7:
            min_index = ponderacions.index(min(ponderacions))
            ponderacions[min_index] += diferencia
        else:
            # Si no, s'afegeix la diferència a la primera ponderació
            ponderacions[0] += diferencia

    # S'afegeix la quarta ponderació amb un valor de 0.1
    ponderacions.append(0.1)

    # Retorna les ponderacions
    return ponderacions


def primera_generacio(passadis, n_individus, id_individu):
    """
    Genera la primera generació d'individus.

    Args:
        passadis (Passadis): Objecte que representa els passadissos disponibles.
        n_individus (int): Nombre d'individus a generar.
        id_individu (int): Identificador únic per als individus.

    Returns:
        list: Llista d'individus generats.
    """

    # Obtenir les entrades del passadís
    entrades = passadis.get_entrades()
    # Crear una llista buida per als individus
    individus = []

    # Per a cada individu en la generació
    for j in range(n_individus):
        # Incrementar l'identificador del individu
        id_individu += 1
        
        # Escollir una entrada aleatòria per a l'individu
        vector_entrada = random.choice(entrades)
        entrada = random.choice(vector_entrada)

        # Calcular la sortida i l'objectiu de l'individu
        sortida = ui.calcul_sortida(entrada, passadis)
        objectiu = ui.calcul_objectiu(entrada, sortida)  

        # Generar ponderacions aleatòries per a l'individu
        ponderacions = generar_ponderacions(4)

        # Escollir un camp de visió aleatori dins d'un rang definit
        camp_visio = 4

        # Crear un nou individu amb els paràmetres generats
        individu = ci.Individu(id_individu, entrada, sortida, objectiu, 1, passadis.get_m(), passadis.get_n(), camp_visio, ponderacions)
        
        # Afegir l'individu a la llista d'individus
        individus.append(individu)
    
    # Tornar la llista d'individus
    return individus


def copiar_individu(ind, passadis, id_individu):
    """
    Copia un individu existent.

    Args:
        ind (Individu): Individu a copiar.
        passadis (Passadis): Objecte que representa els passadissos disponibles.
        id_individu (int): Identificador únic per al nou individu copiat.

    Returns:
        Individu: Nou individu copiat.
    """

    # Obtenir les entrades del passadís
    entrades = passadis.get_entrades()  

    # Obtenir les ponderacions de l'individu
    ponderacions = ind.trajecte.get_ponderacions()

    # Establir el camp de visió
    camp_visio = 4

    # Escollir una entrada aleatòria per a l'individu
    vector_entrada = random.choice(entrades)
    entrada = random.choice(vector_entrada)

    # Calcular la sortida i l'objectiu de l'individu
    sortida = ui.calcul_sortida(entrada, passadis)
    objectiu = ui.calcul_objectiu(entrada, sortida)

    # Crear un nou individu que és una còpia de l'original, però amb un nou identificador
    nou_ind = ci.Individu(id_individu, entrada, sortida, objectiu, 1, ind.m, ind.n, camp_visio, ponderacions)
    return nou_ind


def f_aptitud(ind):
    """
    Calcula l'aptitud d'un individu.

    Args:
        ind (Individu): Individu per al qual es calcula l'aptitud.

    Returns:
        int: Aptitud de l'individu.
    """

    # Obtenir el nombre de col·lisions de l'individu
    colisions = ind.trajecte.get_n_colisions()

    # Obtenir el nombre d'agrupacions de l'individu
    agrupacions = ind.trajecte.get_n_agrupat()

    # Obtenir el temps total que l'individu ha recorregut
    temps_total = ind.trajecte.get_t_recorregut()

    # Calcular la aptitud com el nombre d'agrupacions menys el nombre de col·lisions i el temps total
    aptitud = agrupacions - colisions - temps_total

    # Retornar la aptitud
    return aptitud


# Defineix la funció algorisme_genetic, que executa un algorisme genètic per a optimitzar la forma en què els individus travessen un passadís.
def algorisme_genetic(passadis, n_generacions, n_iteracions, aforament, fps):
    """
    Executa un algorisme genètic per optimitzar la forma en què els individus travessen un passadís.

    Args:
        passadis (Passadis): Objecte que representa els passadissos disponibles.
        n_generacions (int): Nombre de generacions per a executar l'algorisme genètic.
        n_iteracions (int): Nombre d'iteracions per cada generació.
        aforament (int): Capacitat màxima d'individus en el passadís.
        fps (int): Nombre de fotogrames per segon per a la representació gràfica de la simulació.
    """
    
    # Obtenim la matriu sobre la qual es realitzarà la simulació
    matriu = passadis.get_passadis()    

    # Obtenim les entrades i sortides del passadís
    entrades = passadis.get_entrades()      

    # Inicialitzem Pygame i creem un rellotge per controlar el temps
    pygame.init()
    clock = pygame.time.Clock()

    # Obtenim la resolució de la pantalla del dispositiu on s'executa el programa
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w * 0.95
    screen_height = screen_info.current_h * 0.95

    # Calculem les dimensions de les cel·les en funció de la resolució de la pantalla
    cell_width = screen_width // passadis.get_n()
    cell_height = screen_height // passadis.get_m()

    # Seleccionem la mida més petita per mantenir les cel·les quadrades
    cell_size = min(cell_width, cell_height)

    # Ajustem les dimensions de la pantalla per mantenir les cel·les quadrades
    screen_width = cell_size * passadis.get_n()
    screen_height = cell_size * passadis.get_m()

    # Calculem la mida de cada cel·la
    cell_size = (cell_size, cell_size)

    # Creem una finestra a pantalla completa
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    # Inicialitzem algunes llistes i variables que farem servir més endavant
    millors_individus = []
    individus = []
    passadis.ind_in_passadis = []
    nova_generacio = []
    id_individu = 0
    mitjanes_apt = []
    totes_ponderacions = []
    
    # Creem una font que farem servir per mostrar text a la pantalla
    font = pygame.font.Font(None, 24) 

    # Bucle per a la creació i moviment dels individus i representació gráfica de la simulacio
    for gen in range(n_generacions):
        # Inicialitzem llistes d'individus per a cada nova generació
        individus = []
        passadis.ind_in_passadis = []

        if gen > 0:
            # Variable auxiliar per a iterar sobre la llista nova_generacio
            j = 0

        # Comencem el bucle per a cada unitat de temps en la generació (251 iteracions)
        for t in range(n_iteracions):
            # Creem un nombre aleatori d'individus que aniran de 0 al màxim que ens permeti l'aforament
            nous_individus = random.randint(0, (aforament-len(passadis.ind_in_passadis))//10)
            print(f"Nous individus = {nous_individus}\n")

            # Si estem a la primera generació (gen == 0)
            if gen == 0:
                # Creem els individus de la primera generació
                primers_individus = primera_generacio(passadis, nous_individus, id_individu)
                # Afegeix cada nou individu a la llista d'individus i al passadís
                for ind in primers_individus:
                    individus.append(ind)
                    passadis.ind_in_passadis.append(ind)

                    # S'actualitza la posicio de la matriu on ara esta l'individu
                    matriu[individus[-1].get_posicio()] = 1

                    # S'actualitza el diccionari de posicions amb un nou individu
                    passadis.diccionario_posicion[ind.posicio] = ind

                # Incrementem l'ID de l'individu per als futurs individus
                id_individu += len(primers_individus)

            # Si no estem a la primera generació
            if gen > 0:
                # Creem nous individus fins que el nombre d'individus actuals més els nous individus superi la longitud de la nova generació
                while (len(individus) + nous_individus) > len(nova_generacio):
                    # Seleccionem dos dels millors individus a l'atzar per ser pares
                    pare1, pare2 = random.sample(millors_individus, 2)

                    # Creem un nou individu a partir dels dos pares
                    fill = crear_fill(pare1, pare2, passadis, id_individu)
                    id_individu += 1

                    # Afegim el nou individu a la nova generació
                    nova_generacio.append(fill)

                # Afegim els nous individus a la llista d'individus i al passadís, i actualitzem la matriu i el diccionari de posicions
                for _ in range(nous_individus):
                    individus.append(nova_generacio[j])
                    passadis.ind_in_passadis.append(nova_generacio[j])
                    matriu[individus[-1].get_posicio()] = 1
                    passadis.diccionario_posicion[nova_generacio[j].posicio] = nova_generacio[j]
                    j += 1
                
                # Imprimim la longitud de la llista d'individus i el valor de j
                print(f"len(individus) = {len(individus)}\n")
                print(f"j = {j}\n")

            # Movem cada individu al passadís
            for ind in passadis.get_ind_in_passadis():
                ui.moure_individu(ind, passadis)

            # Si un individu ha passat per una entrada, corregim la matriu
            for entrada in entrades:
                for e in entrada:
                    matriu[e] = 3

            # Imprimim la quantitat d'individus en el passadís i en total en aquesta unitat de temps
            print(f"Quantitat d'invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")
            print(f"Total invididus en t = {t} = {len(individus)}\n")

            # Imprimim l'estat de la matriu en aquesta unitat de temps
            print(f"Passadís en t = {t}:\n{matriu}\n")

            # Dibuixem el passadís en cada unitat de temps
            dpygame.dibuixar_passadis(passadis, screen, cell_size, clock, fps)
            
            # Creem un text amb el número de generació actual i el dibuixem a la pantalla
            gen_surface = font.render(f"Generación: {gen}", True, (0, 0, 0))
            screen.blit(gen_surface, (25, 25))

            # Actualitzem la pantalla
            pygame.display.flip()

        # Buidem el passadís
        matriu[1:-1, 1:-1] = 0

        # Inicialitzem diverses variables per recollir dades d'interès
        aptituds = {}  # Diccionari per emmagatzemar les puntuacions d'aptitud
        mitjana_aptitud = 0  # Mitjana d'aptituds
        total_colisions = total_agrupacions = 0  # Total de col·lisions i agrupacions
        ponderacions_totals = [0, 0, 0, 0]  # Llista per emmagatzemar les ponderacions totals

        # Iterem per cada individu
        for ind in individus:
            # Calculem l'aptitud de l'individu i l'emmagatzemem
            aptitud = f_aptitud(ind)
            ind.set_aptitud(aptitud)
            aptituds[ind] = aptitud
            mitjana_aptitud += aptitud  # Incrementem la mitjana d'aptitud amb l'aptitud de l'individu actual

            # Recopilem dades addicionals sobre col·lisions i agrupacions, i actualitzem les ponderacions totals
            total_colisions += ind.trajecte.get_n_colisions()
            total_agrupacions += ind.trajecte.get_n_agrupat()
            ponderacions_totals[0] += ind.trajecte.get_ponderacions()[0]
            ponderacions_totals[1] += ind.trajecte.get_ponderacions()[1]
            ponderacions_totals[2] += ind.trajecte.get_ponderacions()[2]
            ponderacions_totals[3] += ind.trajecte.get_ponderacions()[3]

        # Calculem les ponderacions mitjanes i l'aptitud mitjana
        ponderacions_totals[0] = ponderacions_totals[0] / len(individus)
        ponderacions_totals[1] = ponderacions_totals[1] / len(individus)
        ponderacions_totals[2] = ponderacions_totals[2] / len(individus)
        ponderacions_totals[3] = ponderacions_totals[3] / len(individus)
        mitjana_aptitud = mitjana_aptitud / len(individus)
        mitjanes_apt.append(mitjana_aptitud)

        # Imprimim dades sobre cada individu
        for ind in individus:
            if ind.get_posicio() == None:
                print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()}"+
                    f" ha tingut {ind.trajecte.get_n_colisions()} col·lisions, {ind.trajecte.get_n_agrupat()} moviments agrupat"+
                    f"i ha fet el recorregut en {ind.trajecte.get_t_recorregut()} moviments\n")
                print(f"La puntuació d'aptitud de l'individu {ind.get_id()} = {ind.get_aptitud()}\n")

        # Calculem el nombre total d'individus i imprimim dades globals de la simulació
        len_individus = individus[-1].get_id() + 1
        print(f"En aquesta simulació hi ha hagut un total de {total_colisions} col·lisions i {total_agrupacions} agrupacions entre els {len_individus} individus\n")
        print(f"Per tant, de mitja, hi han hagut {total_colisions/len_individus:.2f} col·lisions i {total_agrupacions/len_individus:.2f} agrupacions\n")
        print(f"La puntuació d'aptitud mitjana = {mitjana_aptitud}\n")
        print(f"P = {ponderacions_totals}\n")
        totes_ponderacions.append(ponderacions_totals)

        # Aquí comença un nou cicle de l'algoritme genètic
        millors_individus = []  # Llista dels millors individus
        nova_generacio = []  # Llista per la nova generació d'individus

        # Filtrar els individus que han completat el recorregut
        aptituds = {ind: apt for ind, apt in aptituds.items() if ind.trajecte.get_recorregut()[-1] is None}

        # Ordenem els individus per aptitud, en ordre descendent
        aptituds_ordenades = dict(sorted(aptituds.items(), key=lambda item: item[1], reverse=True))

        # Calculem el nombre d'individus en el 50% superior
        n_millors = int(len(aptituds_ordenades) / 2)

        # Obtenim el 50% dels individus amb la millor puntuació d'aptitud
        millors_individus = list(aptituds_ordenades.keys())[:n_millors]

        # Si tenim menys de 20 millors individus, aturem el bucle
        if len(millors_individus) < 20:
            break

        # Inicialitzem un contador i una llista per emmagatzemar les ponderacions dels millors individus
        id_individu = 0
        millors_ponderacions = [0, 0, 0, 0]

        # Iterem pels millors individus
        for ind in millors_individus:
            # Actualitzem les ponderacions dels millors individus
            millors_ponderacions[0] += ind.trajecte.get_ponderacions()[0]
            millors_ponderacions[1] += ind.trajecte.get_ponderacions()[1]
            millors_ponderacions[2] += ind.trajecte.get_ponderacions()[2]
            millors_ponderacions[3] += ind.trajecte.get_ponderacions()[3]

            # Copiem el millor individu i l'afegim a la nova generació
            nou_ind = copiar_individu(ind, passadis, id_individu)
            nova_generacio.append(nou_ind)
            id_individu += 1  # Incrementem el comptador d'individus

        # Calculem les ponderacions mitjanes dels millors individus
        millors_ponderacions[0] = millors_ponderacions[0] / len(millors_individus)
        millors_ponderacions[1] = millors_ponderacions[1] / len(millors_individus)
        millors_ponderacions[2] = millors_ponderacions[2] / len(millors_individus)
        millors_ponderacions[3] = millors_ponderacions[3] / len(millors_individus)
        print(f"\nM = {millors_ponderacions}\n")

        # Començar bucle fins que la nova generació sigui de la mateixa mida que l'anterior
        while len(individus) + 1 > len(nova_generacio):
            # Escollir aleatòriament dos individus dels millors per ser pares
            pare1, pare2 = random.sample(millors_individus, 2)

            # Crear un nou individu (fill) a partir de la combinació de les ponderacions dels pares
            fill = crear_fill(pare1, pare2, passadis, id_individu)
            id_individu += 1  # Incrementar l'identificador per al pròxim individu

            # Afegir el nou individu a la nova generació
            nova_generacio.append(fill)

        # Una vegada s'ha creat la nova generació, es realitza una mutació
        nova_generacio = mutar(nova_generacio)
        
        # Mostrar la longitud de la nova generació
        print(f"len(nova_generacio) = {len(nova_generacio)}\n")  
        
        # Pausar durant un segon
        time.sleep(1)  

    # Iterar a través de totes les ponderacions per a cada generació i imprimir-les
    for i in range(len(totes_ponderacions)):
        print(f"Ponderacions en generació {i} = {totes_ponderacions[i]}\n")

    # Crear un gràfic per mostrar la evolució de l'aptitud mitjana
    plt.plot(mitjanes_apt)  # Generar el gràfic amb les mitjanes d'aptitud
    plt.title("Evolución de la aptitud media")  # Afegir títol al gràfic
    plt.xlabel("Generaciones")  # Afegir etiqueta al eix X
    plt.ylabel("Aptitud media")  # Afegir etiqueta al eix Y
    plt.show()  # Mostrar el gràfic


# Definim una funció que creï un nou individu a partir de dos pares
def crear_fill(pare1, pare2, passadis, id):
    """
    Crea un nou individu a partir de dos pares.

    Args:
        pare1 (Individu): Primer pare.
        pare2 (Individu): Segon pare.
        passadis (Passadis): Objecte que representa els passadissos disponibles.
        id (int): Identificador únic per al nou individu.

    Returns:
        Individu: El nou individu creat.
    """

    # Obtenir les entrades possibles del passadís
    entrades = passadis.get_entrades()

    # Obtenir les ponderacions de cada pare
    ponderacions_padre1 = pare1.trajecte.get_ponderacions()
    ponderacions_padre2 = pare2.trajecte.get_ponderacions()
    
    # Donat que el camp de visió és constant obtenim el mateix que un dels pares
    camp_visio = pare1.get_camp_visio()

    # Calcular el punt mitjà de les ponderacions
    meitat = len(ponderacions_padre1) // 2

    # Crear les ponderacions del fill combinant les ponderacions dels pares
    ponderacions_fill = ponderacions_padre1[:meitat] + ponderacions_padre2[meitat:]

    # Normalitzar les ponderacions perquè sumin 1
    suma_total = sum(ponderacions_fill)
    ponderacions_fill = [p/suma_total for p in ponderacions_fill]
    
    # Calcula l'entrada de l'individu escollint una entrada aleatòria
    vector_entrada = random.choice(entrades)
    entrada = random.choice(vector_entrada)

    # Calcular la sortida i l'objectiu de l'individu
    sortida = ui.calcul_sortida(entrada, passadis)
    objectiu = ui.calcul_objectiu(entrada, sortida)  

    # Crear un nou individu amb les ponderacions del fill
    fill = ci.Individu(id, entrada, sortida, objectiu, 1, pare1.m, pare2.n, camp_visio, ponderacions_fill)

    # Retornar el nou individu
    return fill


# Definim una funció que muti una certa percentatge de la població
def mutar(poblacio, percentatge=0.2):
    """
    Mutar una certa percentatge de la població.

    Args:
        poblacio (list): Llista d'individus de la població.
        percentatge (float, opcional): Percentatge d'individus a mutar. El valor per defecte és 0.2.

    Returns:
        list: La població amb les mutacions realitzades.
    """

    # Calcular la quantitat d'individus a mutar
    num_mutacions = int(len(poblacio) * percentatge)

    # Seleccionar aleatòriament els individus a mutar
    individus_a_mutar = random.sample(poblacio, num_mutacions)

    # Per a cada individu a mutar
    for individu in individus_a_mutar:
        # Seleccionar una ponderació a l'atzar, excluint la quarta ponderació
        index_ponderacio = random.randint(0, len(individu.trajecte.get_ponderacions()) - 2)  # '-2' per a excloure la quarta ponderació
        # Calcular una nova ponderació que no faci que la suma de ponderacions superi el 0.9
        nova_ponderacio = random.uniform(0.1, 0.9 - sum([p for i, p in enumerate(individu.trajecte.get_ponderacions()) if i != index_ponderacio and i != 3]))

        # Actualitzar la ponderació de l'individu
        individu.trajecte.get_ponderacions()[index_ponderacio] = nova_ponderacio

    # Retornar la població amb les mutacions realitzades
    return poblacio


# Crear una instància de la classe Passadis amb els paràmetres donats
"""
Paràmentres algorisme genètic
- Identificador únic del passadís (si només es crea un passadís pot ficar sempre 0)
- Valor de m (files)
- Valor de n (columnes)
- Amplada de la entrada (quanitat de cel·les que ocupa cada entrada quan entrada_unica és False)
- Entrada única: és una variable booleana que pot valdre True o False
- Entrades laterals: és una variable booleana que pot valdre True o False
- Obstacles: és una variable booleana que pot valdre True o False
"""
passadis = cp.Passadis(0, 25, 15, 6, True, False, False)

# Executar l'algoritme genètic amb el passadís creat i els paràmetres donats
"""
Paràmentres algorisme genètic
- Passadís
- Quantitat de generacions
- Nombre de iteracions per generació
- Aforament
- Fotogrames per segon
"""
algorisme_genetic(passadis, 10, 250, 50, 40)
