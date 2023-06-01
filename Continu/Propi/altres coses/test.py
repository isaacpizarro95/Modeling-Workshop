import numpy as np
import matplotlib.pyplot as plt

def crear_parets(m, n):
    # # Crea els quatre segments que composen les parets del passadís
    # segment1 = [(0, 0), (m, 0)]  # Paret inferior
    # segment2 = [(0, n), (m, n)] # Paret superior
    # segment3 = [(0, 0), (0, n)] # Paret esquerra
    # segment4 = [(m, 0), (m, n)] # Paret dreta

    min_x = 0
    max_x = m
    min_y = 0
    max_y = n

    # Torna una llista amb tots els segments
    return [min_x, max_x, min_y, max_y]

min_x, max_x, min_y,  max_y = crear_parets(35, 15)
print(f"min_x = {min_x}\nmax_x = {max_x}\nmin_y = {min_y}\nmax_y = {max_y}\n")