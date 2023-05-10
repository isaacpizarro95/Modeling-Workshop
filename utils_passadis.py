import numpy as np
import random
import math

class Paret:
    def __init__(self, inici, final):
        self.inici = inici
        self.final = final

def distancia_a_paret(x,y,paret):
    inici_x, inici_y = paret.inici
    final_x, final_y = paret.final
    distancia_linea = (final_x - inici_x)**2 + (final_y - inici_y)**2

    if distancia_linea == 0:
        return math.sqrt((x - inici_x)**2 + (y - inici_y)**2)
    
    t = ((x - inici_x) * (final_x - inici_x) + (y - inici_y) * (final_y - inici_y)) / distancia_linea

    if t < 0:
        return math.sqrt((x - inici_x)**2 + (y - inici_y)**2)
    elif t > 1:
        return math.sqrt((x - final_x)**2 + (y - final_y)**2)
    
    proj_x = inici_x + t * (final_x - inici_x)
    proj_y = inici_y + t * (final_y - inici_y)

    return math.sqrt((x - proj_x)**2 + (y - proj_y)**2)

def crear_perimetre_parets(m, n, amplada_paret):
    parets = [
        Paret((amplada_paret, amplada_paret), (m - amplada_paret, amplada_paret)),
        Paret((amplada_paret, amplada_paret), (amplada_paret, n - amplada_paret)),
        Paret((m - amplada_paret, amplada_paret), (m - amplada_paret, n - amplada_paret)),
        Paret((amplada_paret, n - amplada_paret), (m -amplada_paret, n -amplada_paret))
    ]

    return parets

def is_inside_paret(x, y, parets, amplada_paret):
    for paret in parets:
        if distancia_a_paret(x, y, paret) < amplada_paret:
            return True
    return False


class Entrada:
    def __init__(self, inici, final):
        self.inici = inici
        self.final = final

def crear_entrades(m, n, amplada_paret):
    entrades = [
        Entrada((amplada_paret, n // 3), (amplada_paret, n // 3 + amplada_paret)),
        Entrada((m - amplada_paret, 2 * n // 3), (m - amplada_paret, 2 * n // 3 + amplada_paret))
    ]
    return entrades

def is_inside_entrada(x, y, entrades, amplada_paret):
    for entrada in entrades:
        if distancia_a_paret(x, y, entrada) < amplada_paret:
            return True
        
    return False


def crear_passadis(m, n, amplada_entrada, entrada_unica, entrades_laterals, obstacles):
    passadis = {}

    # Creem parets, entrades i obstacles
    #amplada_paret = 1 * (min(m, n) / min(20, 15))
    amplada_paret = 1 # De moment establim una amplada igual per tots els tamanys
    parets = crear_perimetre_parets(m, n, amplada_paret)
    entrades = crear_entrades(m, n, amplada_paret)
    obs = []
    #obs = crear_obstacles()

    # FALTA CREAR CÓDIGO AQUÍ PARA INDICAR QUE PUNTOS DEL PASILLO FORMAN PARTE DE UNA PARET O UNA ENTRADA

    return passadis, entrades, parets, obs



# class Obstacle:
#     def __init__(self, inici, final):
#         self.inici = inici
#         self.final = final

# def crear_obstacles(posicions_obstacle):
#     obstacles = [Obstacle(inici, final) for inici, final in posicions_obstacle]
#     return obstacles

# def is_inside_obstacle(x, y, obstacles, amplada_paret):
#     for obstacle in obstacles:
#         if distancia_a_paret(x, y, obstacle) < amplada_paret:
#             return True
#     return False
