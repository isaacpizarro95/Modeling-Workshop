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


# OPCIÓ 2
# def moure_individu(individu, passadis, individus):
#     x, y = individu.get_posicio()
#     objectiu = individu.get_objectiu()
#     vel_actual = individu.get_velocitat()
#     matriu = passadis.get_passadis()
    

#     if((x,y) == objectiu):
#         individu.set_posicio(None)
#         return

#     # Obtenim les posicions vàlides adjacents a la posició actual
#     posicions_valides = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
#     posicions_valides = [pos for pos in posicions_valides if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 1]

#     if not posicions_valides: return

#     # Calculem la posició següent d'acord amb l'algoritme RVO
    
#     #Radi de col·lisió
#     radi_col = 0.2 

#     # Calcula la velocitat de preferència (v_pref) de l'individu basant-se en la velocitat actual (vel_actual) i la direcció cap al seu objectiu (objectiu - posició actual). La direcció es normalitza dividint-ne per la magnitud.
#     v_pref = vel_actual * (np.array(objectiu) - np.array(individu.get_posicio())) / np.linalg.norm(np.array(objectiu) - np.array(individu.get_posicio())) 
    
#     #Llista amb els veins que es poden xocar
#     veins = [] 
#     for ind in individus:
#         if ind.id == individu.id: continue
#         if ind.posicio == None: continue

#         #Afegim una distància màxima (10) per no considerar veins molt llunyans
#         if np.linalg.norm(np.array(ind.get_posicio()) - np.array(individu.get_posicio())) > 10: continue 
        
#         veins.append(ind)
    
#     #Si tenim veins, calculem la nova velocitat
#     if len(veins) > 0: 
#         # La funció "compute_new_velocity" pren com a arguments la posició actual de l'individu, la velocitat de preferència ("v_pref"), una 
#         # llista de veïns propers ("veins"), i el radi de col·lisió ("radi_col"). La funció torna un nou vector de velocitat que representa la 
#         # velocitat que l'individu hauria de tenir per evitar col·lisions amb els veïns propers i moure's cap al seu objectiu.
#         individu.set_velocitat(compute_new_velocity(np.array(individu.get_posicio()), v_pref, veins, radi_col))
    
#     else: #Si no tenim veins seguim amb la mateixa velocitat
#         individu.set_velocitat(v_pref)

#     # Actualitzem la posició segons la nova velocitat
#     nova_posicio = tuple(np.array(individu.get_posicio()) + individu.get_velocitat())
#     if nova_posicio in posicions_valides:
#         individu.set_posicio(nova_posicio)

#     #return np.linalg.norm(new_vel)

# def compute_new_velocity(position, preferred_velocity, neighbors, radius):
#     velocity = preferred_velocity.copy()
#     for neighbor in neighbors:
#         relative_position = neighbor.get_posicio() - position
#         distance = np.linalg.norm(relative_position)
#         if distance < radius:
#             separation_strength = 1.0 - distance / radius
#             velocity -= separation_strength * relative_position / distance
#     return velocity
