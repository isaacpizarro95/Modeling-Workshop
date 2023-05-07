import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt

# En aquest fitxer configurem els diferents passadissos
# Per simplificar la majoria de variables (potser totes) no podran ser modificades un cop creat el passadis
class Passadis:
    def __init__(self, id, m, n, entrada_unica=False, entrades_laterals=False, obstacles=False):
        self.id = id                                        # identificador únic del passadís per diferenciar-lo
        self.m = m                                          # m files
        self.n = n                                          # n carrils (columnes)
        self.num_entrades = random.randint(n//2, 2*n)       # la quantitat d'entrades es calcula de forma aleatoria i pot agafar valors en el interval [2, n)
        self.entrada_unica = entrada_unica                  # True si tot es entrada o False si hi han entrades concretes
        self.entrades_laterals = entrades_laterals
        self.obstacles = obstacles                          # True si posem obstacles i False si no. Podem afegir un altra variable per descriure els obstacles
        self.ind_in_passadis = []

        # Creació del passadís
        self.passadis, self.entrades, self.parets = crear_passadis(m, n, self.num_entrades, entrada_unica, entrades_laterals)

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades
        
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
        


class Trajecte:
    def __init__(self, recorregut, n_colisions, t_recorregut, t_agrupat):
        self.recorregut = recorregut
        self.n_colisions = n_colisions
        self.t_recorregut = t_recorregut
        self.t_agrupat = t_agrupat

    def get_recorregut(self):
        return self.recorregut
    
    def get_n_colisions(self):
        return self.n_colisions
    
    def add_n_colisions(self, nova_colisio): # Afegeix una nova colisio al sumatori de colisions
        self.n_colisions += nova_colisio

    def get_t_recorregut(self):
        return self.t_recorregut
    
    def set_t_recorregut(self, nou_t_recorregut): # Guarda el temps trigat en fer el recorregut
        self.t_recorregut = nou_t_recorregut
    
    def get_t_agrupat(self):
        return self.t_agrupat

    def add_t_agrupat(self): # Suma 1 al temps que l'individu porta agrupat amb altres individus al recorregut
        self.t_agrupat += 1


class Individu:
    def __init__(self, id, posicio, objectiu, velocitat, m, n):
        self.id = id                    # identificador únic per individu
        self.posicio = posicio          # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.objectiu  = objectiu       # dupla(x, y) posició de la sortida/objectiu de l'individu
        self.m = m                      # files passadís
        self.n = n                      # carrils passadís
        self.velocitat_maxima = velocitat 
        #self.velocitat_actual = velocitat
        #self.camp_visio = camp_visio   # dupla de enters (i, j) que indica la distància (en quadrats) màxima a la que pot veure l'individu dins del mapa. i mira la fila, j la columna. El camp de visió no es pot modificar un cop establert     
        self.trajecte = Trajecte([posicio], 0, 0, 0) # conté recorregut, temps recorregut, nombre de col·lisions i temps agrupat        

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.trajecte.recorregut.append(nova_posicio)
    
    def get_objectiu(self):
        return self.objectiu
    
    def get_velocitat(self):
         return self.velocitat

    def set_velocitat(self, nova_velocitat):
        self.velocitat = nova_velocitat

    def get_trajecte(self):
        return self.trajecte



# En el nostre passadís hi han 4 valors diferents:
# 0 si no hi ha individus ni obstacles
# 1 si hi ha un individu
# 2 si és una paret
# 3 si és una entrada/sortida (aquestes només poden apareixer a les parets)
# 4 si és un obstacle

# Variable k per establir la mesura de la entrada en quantitats de quadrats de la matriu

def crear_passadis(m, n, num_entrades, entrada_unica=False, entrades_laterals=False, obstacles=False):
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
    
    # Les entrades i sortides son en si el mateix. Poden entrar i sortir individus per ella.
    # Si entrada_gran == True tota la part superior i tota la part inferior serà entrada/sortida.
    if entrada_unica == True:
        entrades = [p for p in parets if p[0] == 0 or p[0] == (m-1)]
    
    # Si entrades_laterals == False només hi hauran entrades a la part superior i inferior del passadís.
    elif entrades_laterals == False:
        entrades = random.sample([p for p in parets if p[0] == 0 or p[0] == (m-1)], num_entrades)
    
    else:
        entrades = random.sample(parets, num_entrades)
    
    for entrada in entrades:
        x, y = entrada
        passadis[x, y] = 3

    elements = [passadis, entrades, parets]
    return elements

# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(entrada, entrades):
    posibles_sortides = [sortida for sortida in entrades if sortida[0] != entrada[0] and sortida != entrada] # Afegir avaluació de la fila
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

    if((x,y) == objectiu):
        individu.set_posicio(None)
        passadis.ind_in_passadis.remove(individu)
        return
    
    # Obtenim les posicions vàlides adjacents a la posició actual
    posicions_valides = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1)]
    posicions_valides = [pos for pos in posicions_valides if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 1]

    if not posicions_valides:
        return

    # Calculem la distància euclidiana entre les posicions vàlides i l'objectiu
    distancies = [((pos[0] - objectiu[0])**2 + (pos[1] - objectiu[1])**2)**0.5 for pos in posicions_valides]

    # Seleccionem la direcció amb la distància més curta a l'objectiu
    direccio_escollida = posicions_valides[np.argmin(distancies)]

    # Si la direcció escollida és una entrada/sortida, l'individu arriba al seu objectiu i eliminem la seva posició
    if direccio_escollida in passadis.get_entrades() and individu.get_objectiu() == direccio_escollida:
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
    entrades = passadis.get_entrades()

    for x,y in parets:
        if(x,y) in passadis.get_parets():
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.5)) #Parets
        
        else:
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black')) #Cantonades

        if (x,y) in entrades:
            if passadis.get_entrada_unica() == True:
                if x == 0: color = 'blue'
                else: color = 'green'
            else:
                colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                color = colors[passadis.entrades.index((x,y)) % len(colors)]
            plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=200, color=color)

    # Dibuixem els individus amb els colors corresponents
    for ind in individus:
        if ind.posicio == None: continue

        entrada = ind.get_recorregut()[0]
        if passadis.get_entrada_unica() == True:
            if entrada[0] == 0: color = 'blue'
            else: color = 'green'
        else:
            colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
            color = colors[passadis.entrades.index(entrada) % len(colors)] # Calculem el color que li toca al individu a partir de la seva entrada
        x, y = ind.get_posicio()
        plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=100, color=color) # Pintem el color de l'individu en la posició que es troba


    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #plt.get_current_fig_manager().full_screen_toggle()

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    plt.pause(0.15)
    plt.clf()


def simulacio_2D(id_passadis, m, n, num_iteracions, aforament, entrada_unica=False, entrades_laterals=False):
    passadis = Passadis(id_passadis, m, n, entrada_unica, entrades_laterals)    # Hem creat un objecte "Passadís" amb la configuració donada pels paràmetres
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
            objectiu = calcul_sortida(entrada, entrades)
            velocitat = calcul_velocitat()
            individu = Individu(id_individu, entrada, objectiu, velocitat, m, n)
            individus.append(individu)
            passadis.ind_in_passadis.append(individu)
            matriu[individus[-1].get_posicio()] = 1 # Crear una funció per a que només fiqui 1 a la posició si el valor anterior era 0
        
        # Quan un individu passa per una entrada marca com a 1 la posició en la matriu, ho corregim
        for entrada in entrades:
            matriu[entrada] = 3

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dibuixar_passadis(n, m, passadis, individus, t)
        
        # Imprimim l'estat de la matriu en cada unitat de temps 't'
        print(f"Passadís en t = {t}:\n{matriu}\n")

        for ind in individus:
            if ind.get_posicio() is not None:
                moure_individu(ind, passadis)
    
    for ind in individus:
        print(f"L'individu {ind.get_id()}, amb objectiu {ind.get_objectiu()} ha fet el recorregut:\n{ind.trajecte.get_recorregut()}\n")
        

# Recordem el prototip de la funció simulacio_2D:
#   simulacio_2D(id_passadis, m, n, num_iteracions, aforament, entrada_unica=False, entrades_laterals=False)
        # id_passadis = identificador de cada objecte 'passadís'
        # m = nombre de files del passadís
        # n = nombre de columnes/carrils del passadís
        # num_iteracions = "temps" que dura la simulació abans de parar
        # aforament = capacitat màxima que pot tenir el passadís
        # entrada_unica = True si tota la part de dalt i abaix és entrada, False si no és així
        # entrades_laterals = True si hi han entrades a les parets laterals, False si no és així

# Cadena de simulacions
simulacio_2D(0, 10, 10, 20, 30) # Passadís 10*10, normal i aforo = 30
time.sleep(3)
simulacio_2D(1, 10, 10, 20, 30, False, True) # Passadís 10*10, amb entrades laterals i aforo = 30
time.sleep(3)
simulacio_2D(2, 10, 10, 20, 30, True) # Passadís 10*10, amb entrada única i aforo = 30
time.sleep(3)
simulacio_2D(3, 10, 20, 20, 40, True) # Passadís 10*20 amb entrada única i aforo = 30
time.sleep(3)
simulacio_2D(4, 10, 20, 20, 100, True) # Passadís 10*20 amb entrada única i aforo = 100
time.sleep(3)
simulacio_2D(5, 10, 6, 20, 40, True) # passadís 10*6 amb entrada única i aforo = 40
time.sleep(3)
simulacio_2D(6, 30, 40, 60, 100, True) # Passadís 30*40 amb entrada única i aforo = 100
