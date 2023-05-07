import random
import classe_individus as ci
import classe_passadis as cp
import dibuixar_passadis as dp
import utils_individus as ui

def simulacio_2D(passadis, num_iteracions, aforament):
    #passadis = cp.Passadis(id_passadis, m, n, entrada_unica, entrades_laterals)    # Hem creat un objecte "Passadís" amb la configuració donada pels paràmetres
    matriu = passadis.get_passadis()    # Obtenim la matriu sobre la que es farà la simulació
    entrades = passadis.get_entrades()  # Obtenim les entrades/sortides del passadís

    # Informació dels individus
    id_individu = 0     # Creem la variable que distingirà als diferents individus
    individus = []      # Creem una llista per guardar individus

    # Simulem el moviment dels individus a cada interació
    for t in range(num_iteracions):

        # Creem un nombre aleatori d'individus que anirá de 0 al màxim que ens permeti l'aforament' tenint en compte els individus que ja hi han 
        nous_individus = random.randint(0, aforament-len(passadis.ind_in_passadis))
        print(f"Quantitat d'invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")

        # Afegim els individus nous que apareixen a les entrades i els afegim a la llista
        for j in range(nous_individus):
            id_individu += 1
            vector_entrada = random.choice(entrades)
            entrada = random.choice(vector_entrada)
            #entrada = random.choice(entrades)

            sortida = ui.calcul_sortida(entrada, passadis)
            objectiu = ui.calcul_objectiu(entrada, sortida)
            #objectiu = ui.calcul_sortida(entrada, entrades)

            #velocitat = ui.calcul_velocitat()
            velocitat = 1 # s'ha de veure si es necessari que sigui diferent per cada individu
            camp_visio = 5 # s'ha de veure si es necessari que sigui diferent per cada individu

            ponderacions = [1, 2, 1.5, 0.35] # Aquestes ponderacions hauran de venir dels individus de l'anterior generació
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
        dp.dibuixar_passadis(passadis.get_n(), passadis.get_m(), passadis, individus, t)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")

        for ind in individus:
            if ind.get_posicio() is not None:
                ui.moure_individu(ind, passadis)
    
    for ind in individus:
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()} i velocitat {ind.get_velocitat()}"+
              f" ha tingut {ind.trajecte.get_n_colisions()} col·lisions i {ind.trajecte.get_n_agrupat()} moviments agrupat.")
        print(f"Ha fet en {ind.trajecte.get_t_recorregut()} segons el recorregut:\n{ind.trajecte.get_recorregut()}\n\n")