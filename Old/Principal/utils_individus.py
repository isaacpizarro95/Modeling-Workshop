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


# Calcula la velocitat màxima que podrà tenir un individu
def calcul_velocitat():
    velocitats = [0.25, 0.5, 0.75, 1]
    probabilitats = [0.15, 0.25, 0.35, 0.25]

    # La funció np.random.choice pren com a argument la llista de valors possibles (velocitats) i la distribució discreta de probabilitats 
    # corresponent (probabilitats). L'argument p indica les probabilitats corresponents a cada valor de la llista.
    velocitat = np.random.choice(velocitats, p=probabilitats)
    
    return velocitat


# Calcula la distancia euclidiana entre dos punts del passadís
def distancia_euclidiana(a, b):
    return ((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5


# Calcula la direcció de l'individu
def calcul_direccio(pos, obj):
    dx = obj[0] - pos[0]
    dy = obj[1] - pos[1]

    distancia = distancia_euclidiana(pos, obj)

    dir_x = dx / distancia
    dir_y = dy / distancia

    return (dir_x, dir_y)

# Calcula el radi màxim que pot assolir l'individu
def radi_dinamic(individu, m, n):
    max_radi = 10
    x, y = individu.get_posicio()
    
    esquerra = min(y, max_radi)
    dreta = min(n - y - 1, max_radi)
    dalt = min(x, max_radi)
    baix = min(m - x - 1, max_radi)
    
    return min(esquerra, dreta, dalt, baix)

def calcul_objectiu(posicio, sortida):
    aux = distancia_euclidiana(posicio, sortida[0])
    objectiu = sortida[0]
    for pos in sortida:
        if distancia_euclidiana(posicio, pos) < aux:
            objectiu = pos
            aux = distancia_euclidiana(posicio, pos)

    return objectiu


def direccio_mitja(individu, individus, radi, alpha = 0.5):
    # alpha: Quan més proper a 0 donem prioritat a l'objectiu i quan mes proper a 1 donem prioritat al moviment respecte als veins (agruparse)
    total_x = 0
    total_y = 0
    i = 0
    posicio = individu.get_posicio()

    for ind in individus:
        if ind != individu:
            dist = distancia_euclidiana(posicio, ind.get_posicio())
            if dist <= radi:
                total_x += ind.get_posicio()[0]
                total_y += ind.get_posicio()[1]
                i += 1
    
    if i > 0:
        mitja_x = total_x / i
        mitja_y = total_y / i

    else: 
        mitja_x = posicio[0]
        mitja_y = posicio[1]

    objectiu = calcul_objectiu(posicio, individu.get_sortida())
    individu.set_objectiu(objectiu)

    combinacio_x = alpha * mitja_x + (1 - alpha) * objectiu[0]
    combinacio_y = alpha * mitja_y + (1 - alpha) * objectiu[1]

    return (combinacio_x, combinacio_y)

def moure_individu(individu, passadis):
    x, y = individu.get_posicio()
    objectiu = individu.get_objectiu()
    matriu = passadis.get_passadis()
    individus = passadis.get_ind_in_passadis()

    if (x, y) == objectiu:
        individu.set_posicio(None)
        passadis.ind_in_passadis.remove(individu)
        return

    # Obtenim les posicions vàlides adjacents a la posició actual
    posicions_valides = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1)]
    posicions_valides = [pos for pos in posicions_valides if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 1 and matriu[pos] != 4]

    if not posicions_valides:
        return

    # Obtenemos el radio dinámico y la dirección media
    radi = radi_dinamic(individu, passadis.get_m(), passadis.get_n())
    direccio = direccio_mitja(individu, individus, radi)

    # Calculamos la proyección de las posiciones válidas en la dirección media
    proyecciones = [((pos[0] - x) * direccio[0] + (pos[1] - y) * direccio[1]) for pos in posicions_valides]

    # Seleccionamos la posición con la proyección más alta en la dirección media
    #posicio_escollida = posicions_valides[np.argmin(proyecciones)]
    if objectiu[0] == 0: posicio_escollida = posicions_valides[np.argmin(proyecciones)]
    else: posicio_escollida = posicions_valides[np.argmax(proyecciones)]
    
    # Si la posició escollida és una entrada/sortida, l'individu arriba al seu objectiu i eliminem la seva posició
    if posicio_escollida in passadis.get_entrades() and posicio_escollida in objectiu:
        individu.set_posicio(posicio_escollida)
        matriu[x, y] = 0
    else:
        # Actualitzem la posició de l'individu i la matriu
        matriu[x, y] = 0
        matriu[posicio_escollida] = 1
        individu.set_posicio(posicio_escollida)