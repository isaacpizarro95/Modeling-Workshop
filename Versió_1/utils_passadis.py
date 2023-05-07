import numpy as np
import random

# En el nostre passadís hi han 4 valors diferents:
# 0 si no hi ha individus ni obstacles
# 1 si hi ha un individu
# 2 si és una paret
# 3 si és una entrada/sortida (aquestes només poden apareixer a les parets)
# 4 si és un obstacle

# Variable k per establir la mesura de la entrada en quantitats de quadrats de la matriu

def crear_passadis(m, n, num_entrades, entrada_unica=False, entrades_laterals=False, obstacles=False):
    # Creem una matriu de zeros de m files i n columnes (m serà la llargada del passadís i n els carrils)
    passadis = np.zeros((m, n))

    # Afegim "parets" al passadís.
    parets = []
    for i in range(m):
        for j in range(n):
            if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
                if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                    passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
                else:
                    passadis[i, j] = 2  # Perímetre
                    parets.append((i, j))
    
    # Les entrades i sortides son en si el mateix. Poden entrar i sortir individus per ella.
    # Si entrada_gran == True tota la part superior i tota la part inferior serà entrada/sortida.
    if entrada_unica == True:
        entrades = [p for p in parets if p[0] == 0 or p[0] == (m-1)]
    
    # Si entrades_laterals == False només hi hauran entrades a la part superior i inferior del passadís.
    elif entrades_laterals == False:
        entrades = random.sample([p for p in parets if p[0] == 0 or p[0] == (m-1)], num_entrades)
    
    else:
        entrades = random.sample(parets, num_entrades)
    
    for entrada in entrades:
        x, y = entrada
        passadis[x, y] = 3

    elements = [passadis, entrades, parets]
    return elements