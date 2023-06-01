import numpy as np
import utils_passadis as up


def calcul_posicions_entrada(m, n, radi, delta):
    # Crear una lista de todas las posiciones posibles dentro de las entradas
    posiciones = []
    for x in np.arange(radi, m, 2*radi):
        posiciones.append((x, delta))
        posiciones.append((x, n - delta))
    
    # Torna una llista amb tots els segments y las posiciones
    return posiciones


# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(ind_entrada, entrades):
    for entrada in entrades:
        if up.esta_dins_segment(ind_entrada, entrada): continue
        else: return entrada


# Genera una posición aleatoria en la salida seleccionada
def calcul_objectiu(sortida):
    x = round(np.random.uniform(sortida[0][0], sortida[1][0]),2)
    y = round(np.random.uniform(sortida[0][1], sortida[1][1]),2)

    return (x, y)


# Calcula la velocitat preferida d'un individu
def calcul_velocitat_inicial(v_min, v_max):
    # Genera una magnitud de velocitat aleatoria en el rang [v_min, v_max]
    magnitud = np.random.uniform(v_min, v_max)

    # Genera una direcció de velocitat aleatoria en el rang [0, 2π]
    direccio = np.random.uniform(0, 2 * np.pi)

    # Calcula las componentes x e y de la velocidad
    vx = magnitud * np.cos(direccio)
    vy = magnitud * np.sin(direccio)

    return np.array((vx, vy))