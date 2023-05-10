import random
import numpy as np

def crear_pasillo(longitud, ancho, anchura_entrada, entrada_unica, entradas_laterales, obstacles):
    pasillo = {}
    paredes = []
    entradas = []
    obstaculos = []

    # Crear paredes
    for i in range(2):
        for j in range(ancho):
            if i == 0:
                paredes.append((0, j))
            else:
                paredes.append((longitud, j))

    # Crear entradas
    entradas, paredes = crear_entradas(longitud, ancho, paredes, anchura_entrada, entrada_unica, entradas_laterales)

    # Crear obstáculos
    if obstacles:
        num_obstaculos = random.randint(2, 6)
        for _ in range(num_obstaculos):
            x = random.uniform(0, longitud)
            y = random.uniform(0, ancho)
            obstaculos.append((x, y))

    for entrada in entradas:
        pasillo['entrada'] = entrada

    for pared in paredes:
        pasillo['pared'] = pared

    for obstaculo in obstaculos:
        pasillo['obstaculo'] = obstaculo

    return pasillo, entradas, paredes, obstaculos

def crear_entradas(longitud, ancho, paredes_original, anchura_entrada, entrada_unica, entradas_laterales):
    entradas = []
    paredes = paredes_original.copy()

    if entrada_unica:
        entradas.append([p for p in paredes if p[0] == 0])
        entradas.append([p for p in paredes if p[0] == longitud])
    else:
        # ... El resto del código de creación de entradas. Es el mismo que en la versión discreta,
        # pero utilizando coordenadas continuas en lugar de índices de matriz ...

    for entrada in entradas:
        for e in entrada:
            if e in paredes:
                paredes.remove(e)

    return entradas, paredes

