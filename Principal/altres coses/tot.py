import random
import numpy as np
import matplotlib.pyplot as plt


# En aquest fitxer configurem els diferents passadissos
# Per simplificar la majoria de variables (potser totes) no podran ser modificades un cop creat el passadis
class Passadis:
    def __init__(self, id, m, n, amplada_entrada = 1, entrada_unica=False, entrades_laterals=False, obstacles=False):
        self.id = id                                        # identificador únic del passadís per diferenciar-lo
        self.m = m                                        # m files (sumem 2 files per les parets)
        self.n = n                                        # n carrils (columnes) (sumem 2 columnes per les parets)
        self.amplada_entrada = amplada_entrada              # enter que determina quantes cel·les ocupa cada entrada
        # la quantitat d'entrades es calcula de forma aleatoria i pot agafar valors en el interval [a, b)
        #if entrada_unica == True:
        self.num_entrades = random.randint(n//amplada_entrada, ((2*n)-4)//amplada_entrada)  
        #else: self.num_entrades = random.randint(m//amplada_entrada, ((2*(n+m))-4)//amplada_entrada)
        self.entrada_unica = entrada_unica                  # True si tot es entrada o False si hi han entrades concretes
        self.entrades_laterals = entrades_laterals          # True si hi han entrades als laterals o False si no n'hi han
        self.obstacles = obstacles                          # True si posem obstacles i False si no. Podem afegir un altra variable per descriure els obstacles
        self.ind_in_passadis = []                           # Llista dels individus que hi han al passadís a cada instant de temps t

        # Creació del passadís
        self.passadis, self.entrades, self.parets = crear_passadis(m, n, self.amplada_entrada, self.num_entrades, entrada_unica, entrades_laterals)
    
    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades
    
    def get_amplada_entrada(self):
        return self.amplada_entrada

    def get_num_entrades(self):
        return self.num_entrades

    def get_entrada_unica(self):
        return self.entrada_unica
    
    def get_entrades_laterals(self):
        return self.entrades_laterals

    def get_parets(self):
        return self.parets

    def get_passadis(self):
        return self.passadis
    
    def get_ind_in_passadis(self):
        return self.ind_in_passadis
        
# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

class Individu:
    def __init__(self, id, posicio, objectiu, velocitat, m, n):
        self.id = id                    # identificador únic per individu
        self.posicio = posicio          # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.objectiu  = objectiu       # vector [(x_1, y_1),...,(x_n, y_n)] amb les possibles posicions de sortida/objectiu de l'individu
        self.recorregut = [posicio]     # llista(vector) que guarda les posicions en les que ha estat l'individu
        self.m = m                      # files passadís
        self.n = n                      # carrils passadís
        self.velocitat = velocitat      # pot prendre valors: 0.25, 0.5, 0.75, 1. AIXO S'HA DE REDEFINIR
        #self.camp_visio = camp_visio   # dupla de enters (i, j) que indica la distància (en quadrats) màxima a la que pot veure l'individu dins del mapa. i mira la fila, j la columna. El camp de visió no es pot modificar un cop establert     

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)
    
    def get_objectiu(self):
        return self.objectiu
    
    def get_velocitat(self):
         return self.velocitat

    def set_velocitat(self, nova_velocitat):
        self.velocitat = nova_velocitat

    def get_recorregut(self): # Aquesta funció guardarà el recorregut fet per l'usuari pel passadís
        return self.recorregut
        


# En el nostre passadís hi han 4 valors diferents:
# 0 si no hi ha individus ni obstacles
# 1 si hi ha un individu
# 2 si és una paret
# 3 si és una entrada/sortida (aquestes només poden apareixer a les parets)
# 4 si és un obstacle

# Variable k per establir la mesura de la entrada en quantitats de quadrats de la matriu

def crear_passadis(m, n, a_entrada, num_entrades, entrada_unica, entrades_laterals):
    # Creem una matriu de zeros de m files i n columnes (m serà la llargada del passadís i n els carrils)
    passadis = np.zeros((m, n))

    # Afegim "parets" al passadís.
    parets = []
    for i in range(m):
        for j in range(n):
            if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
                if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                    passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
                else:
                    passadis[i, j] = 2  # Perímetre
                    parets.append((i, j))

    entrades, passadis = crear_entrades(m, n, passadis, parets, a_entrada, num_entrades, entrada_unica, entrades_laterals)
    return passadis, entrades, parets

# Les entrades i sortides son en si el mateix. Poden entrar i sortir individus per ella.
def crear_entrades(m, n, passadis, parets_original, a_entrada, num_entrades, entrada_unica, entrades_laterals):
    entrades = []
    parets = parets_original.copy()

    # Si entrades_laterals == False només hi hauran entrades a la part superior i inferior del passadís.
    if entrades_laterals == False:
        parets = [p for p in parets if p[0] == 0 or p[0] == (m-1)]

    posibles_files = [p[0] for p in parets]

    # Si entrada_unica == True tota la part superior i tota la part inferior serà entrada/sortida.
    if entrada_unica == True:
        entrades.append([p for p in parets if p[0] == 0])
        entrades.append([p for p in parets if p[0] == (m-1)])

    else:
        for i in range(num_entrades):
            entrada = []
            
            if entrades_laterals == False:
                if i % 2 == 0: fila = 0 # Podem escollir tenir nomes una entrada a un dels costat i crear un coll d'ampolla
                else: fila = m-1
            else: fila = random.choice(posibles_files)

            if not parets: return entrades, passadis
            p = random.choice([p for p in parets if p[0] == fila])
            entrada.append(p)
            parets.remove(p)

            if (p[1] + a_entrada-1) < (m-1) and (p[0], p[1]+a_entrada-1) in parets:
                for i in range(a_entrada - 1): 
                    entrada.append((p[0], p[1]+i+1))
                    parets.remove((p[0], p[1]+i+1))

            elif (p[1] - a_entrada-1) > 0 and (p[0], p[1]-a_entrada+1) in parets:
                for i in range(a_entrada - 1): 
                    entrada.append((p[0], p[1]-i-1))
                    parets.remove((p[0], p[1]-i-1))

            elif (p[0] + a_entrada-1) < (n-1) and (p[0]+a_entrada-1, p[1]) in parets:
                for i in range(a_entrada - 1): 
                    entrada.append((p[0]+i+1, p[1]))
                    parets.remove((p[0]+i+1, p[1]))

            elif (p[0] - a_entrada-1) > 0 and (p[0]-a_entrada+1, p[1]) in parets:
                for i in range(a_entrada - 1): 
                    entrada.append((p[0]-i-1, p[1]))
                    parets.remove((p[0]-i-1, p[1]))

            else: 
                if a_entrada == 1: entrades.append(entrada)
                else: entrada.remove(p)

            if entrada: entrades.append(entrada)
    
    for entrada in entrades:
        for e in entrada:
            passadis[e] = 3

    return entrades, passadis
    
# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(entrada, passadis):
    entrades = passadis.get_entrades()
    if entrada[0] == 0 or entrada[0] == (passadis.get_m()-1): 
        posibles_sortides = [sortida for sortida in entrades if sortida[0][0] != entrada[0]]
    else:
        posibles_sortides = [sortida for sortida in entrades if sortida[0][1] != entrada[1]]
    return random.choice(posibles_sortides)

# Calcula la velocitat màxima que podrà tenir un individu
def calcul_velocitat():
    velocitats = [0.25, 0.5, 0.75, 1]
    probabilitats = [0.15, 0.25, 0.35, 0.25]

    # La funció np.random.choice pren com a argument la llista de valors possibles (velocitats) i la distribució discreta de probabilitats 
    # corresponent (probabilitats). L'argument p indica les probabilitats corresponents a cada valor de la llista.
    velocitat = np.random.choice(velocitats, p=probabilitats)
    
    return velocitat

#OPCIONS PER MOURE A L'INDIVIDU
# OPCIÓ 1
def moure_individu(individu, passadis):
    x, y = individu.get_posicio()
    objectiu = individu.get_objectiu()
    matriu = passadis.get_passadis()

    if((x,y) in objectiu):
        individu.set_posicio(None)
        passadis.ind_in_passadis.remove(individu)
        return
    
    # Obtenim les posicions vàlides adjacents a la posició actual
    posicions_valides = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1)]
    posicions_valides = [pos for pos in posicions_valides if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 1]

    if not posicions_valides:
        return

    # Calculem la distància euclidiana entre les possibles sortides i la posició actual
    sortides = [((x - sortida[0])**2 + (y - sortida[1])**2)**0.5 for sortida in objectiu]
    sortida_escollida = objectiu[np.argmin(sortides)]

    # Calculem la distància euclidiana entre les posicions vàlides i l'objectiu
    distancies = [((pos[0] - sortida_escollida[0])**2 + (pos[1] - sortida_escollida[1])**2)**0.5 for pos in posicions_valides]
    # Seleccionem la direcció amb la distància més curta a l'objectiu
    direccio_escollida = posicions_valides[np.argmin(distancies)]

    # Si la direcció escollida és una entrada/sortida, l'individu arriba al seu objectiu i eliminem la seva posició
    if direccio_escollida in passadis.get_entrades() and  direccio_escollida in objectiu:
        individu.set_posicio(direccio_escollida)
        matriu[x, y] = 0
    else:
        # Actualitzem la posició de l'individu i la matriu
        matriu[x, y] = 0
        matriu[direccio_escollida] = 1
        individu.set_posicio(direccio_escollida)
        
        
# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, passadis, individus, t):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    # Pintem les vores de color negre per diferenciar els quadrats
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='white', lw=2)
        plt.axhline(i, color='white', lw=2)

    parets = passadis.get_parets()
    parets.extend([(0,0), (0,n-1), (m-1,0), (m-1,n-1)])
    vector_entrades = passadis.get_entrades()
    entrades = [e for entrada in vector_entrades for e in entrada]

    for x,y in parets:
        if(x,y) in passadis.get_parets():
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.5)) #Parets
        
        else:
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black')) #Cantonades

        if (x,y) in entrades:
            for entrada in vector_entrades:
                if (x,y) in entrada:
                    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                    color = colors[vector_entrades.index(entrada) % len(colors)]
            plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=200, color=color)

    # Dibuixem els individus amb els colors corresponents
    for ind in individus:
        if ind.posicio == None: continue
        inici = ind.get_recorregut()[0]

        for entrada in vector_entrades:
            if inici in entrada:
                colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                color = colors[vector_entrades.index(entrada) % len(colors)]
        x, y = ind.get_posicio()
        #if(ind.id == 1): plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=350, color=color) # Util si volem seguir a un en concret
        plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=100, color=color) # Pintem el color de l'individu en la posició que es troba


    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #plt.get_current_fig_manager().full_screen_toggle()

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    if m <= 30: plt.pause(0.75)
    elif 30 < m < 50: plt.pause(0.05)
    else: plt.pause(0.01)
    plt.clf()



def simulacio_2D(passadis, num_iteracions, aforament):
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
            objectiu = calcul_sortida(entrada, passadis)
            velocitat = calcul_velocitat()
            individu = Individu(id_individu, entrada, objectiu, velocitat, passadis.get_m(), passadis.get_n())
            individus.append(individu)
            passadis.ind_in_passadis.append(individu)
            matriu[individus[-1].get_posicio()] = 1 # Crear una funció per a que només fiqui 1 a la posició si el valor anterior era 0
        
        # Quan un individu passa per una entrada marca com a 1 la posició en la matriu, ho corregim
        for entrada in entrades:
            for e in entrada:
                matriu[e] = 3

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dibuixar_passadis(passadis.get_n(), passadis.get_m(), passadis, individus, t)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")

        for ind in individus:
            if ind.get_posicio() is not None:
                moure_individu(ind, passadis)

    for ind in individus:
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()} ha fet el recorregut:\n{ind.get_recorregut()}\n")
