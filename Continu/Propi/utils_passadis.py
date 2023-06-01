import numpy as np
import random
import math

def crear_passadis(m, n):#, amplada_entrada, entrada_unica, entrades_laterals, obstacles):
    # Creem parets, entrades i obstacles
    parets = crear_parets(m, n)
    delta = n/20 # Distància de les entrades respecte la paret en el eix de la y
    entrades = crear_entrades(m, n, delta)
    #obs = crear_obstacles()

    return entrades, parets#, obs

def crear_parets(m, n):
    min_x = 0
    max_x = m
    min_y = 0
    max_y = n

    # Torna una llista amb tots els segments
    return [min_x, max_x, min_y, max_y]

def crear_entrades(m, n, delta):
    # Crear els segments d'entrada i sortida
    entrada1 = [(0, delta), (m, delta)]
    entrada2 = [(0, n - delta), (m, n - delta)]
    
    # Torna una llista amb tots els segments
    return [entrada1, entrada2]

def esta_dins_segment(punt, segment):
    # Calcula la distancia entre el punt i els dos extrems del segment
    dist_a = np.linalg.norm(np.array(punt) - np.array(segment[0]))
    dist_b = np.linalg.norm(np.array(punt) - np.array(segment[1]))

    # Calcula la llargada del segmento
    llargada_segment = np.linalg.norm(np.array(segment[0]) - np.array(segment[1]))

    # Comprova si la suma de les dos distancies és igual a la llargada del segment (amb un cert marge d'error per tindre en compte la precisió de punt flotant)
    if np.isclose(dist_a + dist_b, llargada_segment, rtol=1e-05):
        return True
    else:
        return False