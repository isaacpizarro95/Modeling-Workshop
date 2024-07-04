import numpy as np

def crear_passadis(m, n):
    """
    Crea un passadís amb les entrades i parets corresponents.

    Paràmetres:
    m (int): Dimensió del passadís en l'eix de l'x.
    n (int): Dimensió del passadís en l'eix de l'y.

    Retorna: Les llistes d'entrades i parets.
    """
    # Creem parets
    parets = crear_parets(m, n)

    # Distància de les entrades respecte la paret en el eix de la y
    delta = n/20 

    # Creem entrades
    entrades = crear_entrades(m, n, delta)

    return entrades, parets


def crear_parets(m, n):
    """
    Crea les parets del passadís.

    Paràmetres:
    m (int): Dimensió del passadís en l'eix de l'x.
    n (int): Dimensió del passadís en l'eix de l'y.

    Retorna: Una llista amb les coordenades dels limits de les parets [min_x, max_x, min_y, max_y].
    """
    min_x = 0
    max_x = m
    min_y = 0
    max_y = n

    # Torna una llista amb els límits del passadís
    return [min_x, max_x, min_y, max_y]


def crear_entrades(m, n, delta):
    """
    Crea les entrades del passadís.

    Paràmetres:
    m (int): Dimensió del passadís en l'eix de l'x.
    n (int): Dimensió del passadís en l'eix de l'y.
    delta (float): Distància de les entrades respecte a la paret en l'eix de l'y.

    Retorna: Una llista amb les coordenades dels segments d'entrada i sortida.
    """

    # Crear els segments d'entrada i sortida
    entrada1 = [(0, delta), (m, delta)]
    entrada2 = [(0, n - delta), (m, n - delta)]
    
    # Torna una llista amb tots els segments
    return [entrada1, entrada2]


def esta_dins_segment(punt, segment):
    """
    Comprova si un punt està dins d'un segment.

    Paràmetres:
    punt (dupla): Coordenades del punt a comprovar.
    segment (llista): Coordenades dels extrems del segment [punt1, punt2].

    Retorna:
    bool: True si el punt està dins del segment, False si no ho està.
    """

    # Calcula la distancia entre el punt i els dos extrems del segment
    dist_a = np.linalg.norm(np.array(punt) - np.array(segment[0]))
    dist_b = np.linalg.norm(np.array(punt) - np.array(segment[1]))

    # Calcula la llargada del segment
    llargada_segment = np.linalg.norm(np.array(segment[0]) - np.array(segment[1]))

    # Comprova si la suma de les dos distancies és igual a la llargada del segment (amb un cert marge d'error per tindre en compte la precisió de punt flotant)
    if np.isclose(dist_a + dist_b, llargada_segment, rtol=1e-05):
        return True
    else:
        return False