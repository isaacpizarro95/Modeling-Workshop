import config_individus as ci
import config_passadis as cp
import dibuixar_passadis as dp

# Creem el passadis
id_passadis = 0
m = 8 # nombre de files
n = 3  # nombre de columnes/carrils
passadis = cp.Passadis(0, m, n, 0, n, 0) # Hem creat un objecte "Passadís" amb la configuració donada pels paràmetres
matriu = passadis.get_passadis() # Creem la matriu sobre la que es farà la simulació
e_s = passadis.get_entrades() # Creem les entrades/sortides del passadís
entrades = e_s[0] # Guardem les entrades
sortides = e_s[1] # Guardem les sortides. De moment no les estem utilitzant i no sé si seran necessàries

# Creem la variable que distingirà als diferents individus
id_individu = 0

# Creem una llista per guardar individus
individus = []

# Definim el nombre d'iteracions que tindrà la simulació
num_iteracions = m

# Simulem el moviment dels individus a cada interació
for t in range(num_iteracions):

    #if t == 0:     # apareixen individus nous a les entrades només al principi
    if t % 2 == 0:  # apareixen individus nous a les entrades cada dos unitats de temps
        # Afegim individus nous que apareixen a les entrades i els afegim a la llista
        for j in range(n):
            id_individu += 1
            individus.append(ci.Individu(id_individu, entrades[j], m, n))
            matriu[individus[-1].get_posicio()] = 1

    print("Individus en t =", str(t), ":", len(individus), "\n")
    # Dibuixem el passadís en cada unitat de temps
    dp.dibuixar_passadis(n, m, matriu, individus, t)
    
    # Imprimim l'estat de la matriu en cada unitat de temps 't'
    print("Passadís en t =", str(t), ":\n", matriu, "\n")

    # Movem a cada individu
    for individu in individus:
        if individu.get_posicio() == None:
            continue

        i, j = individu.get_posicio()
        matriu[i, j] = 0 # Borrem la posició anterior

        # Movem els individus en el carril 1 a no ser que estiguin a l'última fila
        if j % 2 == 0 and i != 0:
            individu.moure("puja") # Actualizem la posició de l'individuo
            matriu[individu.get_posicio()] = 1 # Afegim a l'individu a la nova posició

        # Movem els individus en el carril 2 a no ser que estiguin a l'última fila
        elif j % 2 == 1 and i != m-1:
            individu.moure("baixa") # Actualizem la posició de l'individuo
            matriu[individu.get_posicio()] = 1 # Afegim a l'individu a la nova posició
        
        else:
            individu.set_posicio(None) # Potser no es necessari

for ind in individus:
    print("L'individu ", ind.get_id(), " ha fet el recorregut: \n", ind.get_recorregut(), "\n")