import random
import config_individus as ci
import config_passadis as cp
import dibuixar_passadis as dp
import utils_individus as ui

def simulacio_2D(id_passadis, m, n, num_iteracions, aforament, entrada_unica=False, entrades_laterals=False):
    passadis = cp.Passadis(id_passadis, m, n, entrada_unica, entrades_laterals)    # Hem creat un objecte "Passadís" amb la configuració donada pels paràmetres
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
            entrada = random.choice(entrades)
            objectiu = ui.calcul_sortida(entrada, entrades)
            velocitat = ui.calcul_velocitat()
            individu = ci.Individu(id_individu, entrada, objectiu, velocitat, m, n)
            individus.append(individu)
            passadis.ind_in_passadis.append(individu)
            matriu[individus[-1].get_posicio()] = 1 # Crear una funció per a que només fiqui 1 a la posició si el valor anterior era 0
        
        # Quan un individu passa per una entrada marca com a 1 la posició en la matriu, ho corregim
        for entrada in entrades:
            matriu[entrada] = 3

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dp.dibuixar_passadis(n, m, passadis, individus, t)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")

        for ind in individus:
            if ind.get_posicio() is not None:
                ui.moure_individu(ind, passadis)

    for ind in individus:
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()} ha fet el recorregut:\n{ind.get_recorregut()}\n")