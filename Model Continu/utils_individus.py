import numpy as np
import utils_passadis as up

def calcul_posicions_entrada(m, n, radi, delta):
    """
    Calcula les posicions en les quals poden aparèixer els individus al passadís.

    Paràmetres:
    m (int): Dimensió del passadís en l'eix de l'x.
    n (int): Dimensió del passadís en l'eix de l'y.
    radi (float): Radi de l'individu.
    delta (float): Distància de l'entrada respecte a la paret en l'eix de l'y.

    Retorna: Una llista de duples que conté les possibles posicions d'entrada al passadís.
    """

    # Llista on es guarden les possibles posicions per entrar
    posiciones = []

    # L'interval de possibles punts comença en x = radi i acaba en x = m
    # No agafem tota la recta sino que agafem punts amb una distància de 2*radi entre cada punt
    for x in np.arange(radi, m, 2*radi):
        # Posicions de la entrada/sortida de la part inferior del passadís
        posiciones.append((x, delta))
        
        # Posicions de la entrada/sortida de la part superior del passadís
        posiciones.append((x, n - delta))
    
    # Torna una llista amb les possibles posicions en les que es pot aparèixer al passadís
    return posiciones


# Calcula la sortida (segment de punts on es troba l'objectiu)
def calcul_sortida(ind_entrada, entrades):
    """
    Selecciona una de les entrades(accessos) com a sortida

    Paràmetres:
    ind_entrada (dupla): Coordenades de l'entrada de l'individu.
    entrades (llista): Llista amb els segments de les entrades disponibles.

    Retorna: Una llista amb les coordenades del segment de la sortida de l'individu.
    """

    # D'entre els accessos disponibles descarta el accès que és la entrada de l'individu
    for entrada in entrades:
        if up.esta_dins_segment(ind_entrada, entrada): continue
        else: return entrada


# Aquest càlcul de l'objectiu només es dona al principip del trajecte. 
# Després el calcul de l'objectiu es fa a través de trobar el punt més proper a l'individu
def calcul_objectiu(sortida):
    """
    Calcula, a l'inici del trajecte, l'objectiu de l'individu a partir del segment de la sortida.

    Paràmetres:
    sortida (llista): Coordenades del segment de la sortida.

    Retorna:
    dupla: Coordenades de l'objectiu de l'individu.
    """

    x = round(np.random.uniform(sortida[0][0], sortida[1][0]),2)
    y = round(np.random.uniform(sortida[0][1], sortida[1][1]),2)

    return (x, y)


def calcul_velocitat_inicial(v_min, v_max):
    """
    Calcula la velocitat inicial d'un individu.

    Paràmetres:
    v_min (float): Valor mínim de la magnitud de la velocitat.
    v_max (float): Valor màxim de la magnitud de la velocitat.

    Retorna:
    numpy.ndarray: Un vector numpy que representa la velocitat inicial de l'individu.
    """

    # Genera una magnitud de velocitat aleatoria en el rang [v_min, v_max]
    magnitud = np.random.uniform(v_min, v_max)

    # Genera una direcció de velocitat aleatoria en el rang [0, 2π]
    direccio = np.random.uniform(0, 2 * np.pi)

    # Calcula las componentes x e y de la velocidad
    vx = magnitud * np.cos(direccio)
    vy = magnitud * np.sin(direccio)

    return np.array((vx, vy))