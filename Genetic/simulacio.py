import random
import classe_individus as ci
import utils_individus as ui
import dibuixar_pygame as dpygame
import pygame

def simulacio_2D(passadis, num_iteracions, aforament):
    matriu = passadis.get_passadis()    # Obtenim la matriu sobre la que es farà la simulació
    entrades = passadis.get_entrades()  # Obtenim les entrades/sortides del passadís
    mod = passadis.get_mod()

    # Informació dels individus
    id_individu = 0     # Creem la variable que distingirà als diferents individus
    individus = []      # Creem una llista per guardar individus

    # Preparem les variables per la simulació
    pygame.init()
    clock = pygame.time.Clock()

    # Obté el tamany de la pantalla del dispositiu on s'executi el programa
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w * 0.95
    screen_height = screen_info.current_h * 0.95

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

    # Simulem el moviment dels individus a cada interació
    for t in range(num_iteracions):

        # Creem un nombre aleatori d'individus que anirá de 0 al màxim que ens permeti l'aforament' tenint en compte els individus que ja hi han 
        nous_individus = random.randint(0, aforament-len(passadis.ind_in_passadis))
        print(f"Quantitat d'invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")

        # Afegim els individus nous que apareixen a les entrades i els afegim a la llista
        for j in range(nous_individus):
            id_individu += 1
            
            if mod == 'defecte':
                vector_entrada = random.choice(entrades)
                entrada = random.choice(vector_entrada)

                sortida = ui.calcul_sortida(entrada, passadis)
                objectiu = ui.calcul_objectiu(entrada, sortida)
                
            elif mod == 'coll_ampolla':
                vector_entrades = [e for entrada in entrades for e in entrada if e[0] == passadis.get_m()-1]
                entrada = random.choice(vector_entrades)

                sortida = [e for entrada in entrades for e in entrada if entrada[0][0] == 0]
                objectiu = random.choice(sortida)

            #velocitat = ui.calcul_velocitat()
            velocitat = 1 # s'ha de veure si es necessari que sigui diferent per cada individu
            camp_visio = 5  # s'ha de veure si es necessari que sigui diferent per cada individu

            ponderacions = [0.5, 1, 0.75, 0.25] # Aquestes ponderacions hauran de venir dels individus de l'anterior generació
            individu = ci.Individu(id_individu, entrada, sortida, objectiu, velocitat, passadis.get_m(), passadis.get_n(), camp_visio, ponderacions)
            individus.append(individu)
            passadis.ind_in_passadis.append(individu)
            matriu[individus[-1].get_posicio()] = 1 # Crear una funció per a que només fiqui 1 a la posició si el valor anterior era 0
            passadis.diccionario_posicion[individu.posicio] = individu
        
        # Quan un individu passa per una entrada marca com a 1 la posició en la matriu, ho corregim
        for entrada in entrades:
            for e in entrada:
                matriu[e] = 3

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        #dp.dibuixar_passadis(passadis.get_n(), passadis.get_m(), passadis, individus, t)
        dpygame.dibuixar_passadis_pygame(passadis.get_n(), passadis.get_m(), passadis, individus, screen, cell_size, clock)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")

        for ind in individus:
            if ind.get_posicio() is not None:
                ui.moure_individu(ind, passadis)
    
    total_colisions = total_agrupacions = 0
    for ind in individus:
        total_colisions += ind.trajecte.get_n_colisions()
        total_agrupacions += ind.trajecte.get_n_agrupat()

        #Calculem l'aptitud de l'individu dels individus que han arribat al seu objectiu
        # trajecte = ind.get_trajecte()
        # if trajecte.get_recorregut[-1] == None:
        #     aptitud = ui.funcio_aptitud(trajecte, passadis.get_m(), passadis.get_n())
        #     ind.set_aptitud(aptitud)
        
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()} i velocitat {ind.get_velocitat()}"+
              f" ha tingut {ind.trajecte.get_n_colisions()} col·lisions i {ind.trajecte.get_n_agrupat()} moviments agrupat.\n")
        print(f"La puntuació d'aptitud de l'individu {ind.get_id()} = {ind.get_aptitud()}\n")
        print(f"Ha fet en {ind.trajecte.get_t_recorregut()} segons el recorregut:\n{ind.trajecte.get_recorregut()}\n\n")


    
    len_individus = individus[-1].get_id()
    print(f"En aquesta simulació hi ha hagut un total de {total_colisions} col·lisions i {total_agrupacions} agrupacions entre els {len_individus} individus\n")
    print(f"Per tant, de mitja, hi han hagut {total_colisions/len_individus:.2f} col·lisions i {total_agrupacions/len_individus:.2f} agrupacions\n")