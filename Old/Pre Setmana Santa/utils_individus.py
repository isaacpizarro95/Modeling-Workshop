import numpy as np
import random

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