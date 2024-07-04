import random
import classe_individus as ci
import utils_individus as ui
import dibuixar_pygame as dpygame
import pygame

def simulacio(passadis, num_iteracions, aforament, fps, screen_width, screen_height):
    """
    Realitza una simulació en 2D del passadís amb individus en moviment.

    Paràmentres:
    passadis (Passadis): L'objecte passadís que conté la configuració del passadís.
    num_iteracions (int): El nombre total d'iteracions de la simulació.
    aforament (int): El límit d'aforament del passadís.
    fps (int): El nombre de fotogrames per segon per a la simulació.
    """

    # Matriu sobre la que es farà la simulació
    matriu = passadis.get_passadis()    

    # Entrades/sortides del passadís
    entrades = passadis.get_entrades()  

    # Creem la variable que distingirà als diferents individus
    id_individu = 0     

    # Determinem la velocitat i el camp de visio per a tots els individus
    velocitat = 1 
    camp_visio = 5

    # Creem una llista per guardar individus
    individus = []      

    # Preparem les variables per la simulació
    #pygame.init()
    clock = pygame.time.Clock()

    # Calcula el tamany de les cel·les en funció del tamany de la pantalla
    cell_width = screen_width // passadis.get_n()
    cell_height = screen_height // passadis.get_m()

    # Tria el tamany més petit per mantindre les cel·les quadrades
    cell_size = min(cell_width, cell_height)

    # Ajusta el tamany de la pantalla per mantenir les cel·les quadrades
    screen_width = cell_size * passadis.get_n()
    screen_height = cell_size * passadis.get_m()

    # Calcula el tamany de cada cel·la
    cell_size = (cell_size, cell_size)

    # Crea una finestra de pantalla completa
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    # Bucle per a la creacio i moviment dels individus i representacio gráfica de la simulacio
    for t in range(num_iteracions):

        # Creem un nombre aleatori d'individus que anirá de 0 al maxim que ens permeti l'aforament' tenint en compte els individus que ja hi han 
        nous_individus = random.randint(0, (aforament-len(passadis.ind_in_passadis))//10)
        print(f"Quantitat d'invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")

        # Afegim els individus nous que apareixen a les entrades i els afegim a la llista
        for j in range(nous_individus):
            id_individu += 1
            
            # Calcula la entrada de l'individu
            vector_entrada = random.choice(entrades)
            entrada = random.choice(vector_entrada)

            # Calcula la sortida i l'objectiu de l'individu
            sortida = ui.calcul_sortida(entrada, passadis)
            objectiu = ui.calcul_objectiu(entrada, sortida)  

            # Coeficients de importancia per al calcul de les puntuacions de les posicions
            ponderacions = [0.2, 0.4, 0.3, 0.1]

            # Crea l'individu
            individu = ci.Individu(id_individu, entrada, sortida, objectiu, velocitat, passadis.get_m(), passadis.get_n(), camp_visio, ponderacions)
            
            # S'afegeix l'individu al total d'individus
            individus.append(individu)

            # S'afegeix l'individu a la llista d'individus que actualment estan al passadis
            passadis.ind_in_passadis.append(individu)

            # S'actualitza la posicio de la matriu on ara esta l'individu
            matriu[individus[-1].get_posicio()] = 1

            # S'actualitza el diccionari de posicions amb un nou individu
            passadis.diccionario_posicion[individu.posicio] = individu
        
        # Movem als individus
        for ind in passadis.get_ind_in_passadis():
            ui.moure_individu(ind, passadis)

        # Quan un individu passa per una entrada marca com a 1 la posició en la matriu, ho corregim
        for entrada in entrades:
            for e in entrada:
                matriu[e] = 3

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dpygame.dibuixar_passadis(passadis, screen, cell_size, clock, fps)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")


    # Imprimim informació rellevant de la simulació un cop aquesta ha acabat
    total_colisions = total_agrupacions = 0
    for ind in individus:
        total_colisions += ind.trajecte.get_n_colisions()
        total_agrupacions += ind.trajecte.get_n_agrupat()
        
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()}"+
              f" ha tingut {ind.trajecte.get_n_colisions()} col·lisions i {ind.trajecte.get_n_agrupat()} moviments agrupat.\n")
        print(f"La puntuació d'aptitud de l'individu {ind.get_id()} = {ind.get_aptitud()}\n")
        print(f"Ha fet en {ind.trajecte.get_t_recorregut()} segons el recorregut:\n{ind.trajecte.get_recorregut()}\n\n")

    len_individus = individus[-1].get_id() + 1
    print(f"En aquesta simulació hi ha hagut un total de {total_colisions} col·lisions i {total_agrupacions} agrupacions entre els {len_individus} individus\n")
    print(f"Per tant, de mitja, hi han hagut {total_colisions/len_individus:.2f} col·lisions i {total_agrupacions/len_individus:.2f} agrupacions\n")