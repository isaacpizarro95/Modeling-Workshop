import numpy as np
import random

# En el nostre passadís hi han 4 valors diferents:
# 0 si no hi ha individus ni obstacles
# 1 si hi ha un individu
# 2 si és una paret
# 3 si és una entrada/sortida (aquestes només poden apareixer a les parets)
# 4 si és un obstacle

# Variable k per establir la mesura de la entrada en quantitats de quadrats de la matriu

def crear_passadis(m, n, mod, a_entrada, num_entrades, entrada_unica, entrades_laterals, obstacles):
    # Creem una matriu de zeros de m files i n columnes (m serà la llargada del passadís i n els carrils)
    passadis = np.zeros((m, n))

    # Afegim "parets" al passadís.
    parets = []
    if mod == 'coll_ampolla':
        for i in range(m):
            for j in range(n):
                if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
                    if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                        passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
                    else:
                        passadis[i, j] = 2  # Perímetre
                        parets.append((i, j))
                
                if i == int(m/2) and j != int(n/3) and j != (int(n/3)+int(n/3)):#and j != int(n/2)-1 and j != int(n/2) and j != int(n/2)+1:
                        passadis[i, j] = 2
                        parets.append((i, j))                   
    else:     
        for i in range(m):
            for j in range(n):
                if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
                    if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                        passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
                    else:
                        passadis[i, j] = 2  # Perímetre
                        parets.append((i, j))

    entrades, passadis = crear_entrades(m, n, mod, passadis, parets, a_entrada, num_entrades, entrada_unica, entrades_laterals)


    # Creem un nombre aleatori entre 2 i 6 (nombres arbitraris) d'obstacles
    obs = []
    if obstacles == True:
        obs = [(int(m/2), int(n/2)), (int(m/2-1), int(n/2)), (int(m/2), int(n/2+1)), (int(m/2-1), int(n/2+1)), (int(m/2), int(n/2-1)), (int(m/2-1), int(n/2-1))]
        for ob in obs:
            passadis[ob] = 4
    # if obstacles == True:
    #     possibles_obstacles = [np.argwhere(passadis == 0)]
    #     for i in range(random.randint(2,6)):
    #         ob = tuple(random.choice(possibles_obstacles[0]))
    #         passadis[ob] = 4
    #         obs.append(ob)

    return passadis, entrades, parets, obs

# Les entrades i sortides son en si el mateix. Poden entrar i sortir individus per ella.
def crear_entrades(m, n, mod, passadis, parets_original, a_entrada, num_entrades, entrada_unica, entrades_laterals):
    entrades = []
    parets = parets_original.copy()

    #if mod == 'defecte':
    # Si entrades_laterals == False només hi hauran entrades a la part superior i inferior del passadís.
    if entrades_laterals == False:
        parets = [p for p in parets if p[0] == 0 or p[0] == (m-1)]

    #posibles_files = [p[0] for p in parets]

    # Si entrada_unica == True tota la part superior i tota la part inferior serà entrada/sortida.
    if entrada_unica == True:
        entrades.append([p for p in parets if p[0] == 0])
        entrades.append([p for p in parets if p[0] == (m-1)])

    else:
        entrada1 = [] 
        entrada2 = [] 
        entrada3 = [] 
        entrada4 = []
        if entrades_laterals == True:
            for i in range(a_entrada):
                entrada1.append((0, int(n/2) + i - 1))
                entrada2.append((m-1, int(n/2) + i - 1))
                entrada3.append((int(m/2) + i - 1, 0))
                entrada4.append((int(m/2) + i - 1, n-1))            
        else:
            for i in range(a_entrada):
                entrada1.append((m - 1, int((n-1)/3) + i - 1))
                entrada2.append((m - 1, int((n-1)/3) * 2 + i - 1))
                entrada3.append((0, int((n-1)/3) + i - 1))
                entrada4.append((0, int((n-1)/3) * 2 + i - 1))

        entrades.append(entrada1)
        entrades.append(entrada2)
        entrades.append(entrada3)
        entrades.append(entrada4)
        # else:
        #     for i in range(num_entrades):
        #         entrada = []
                
        #         if entrades_laterals == False:
        #             if i % 2 == 0: fila = 0 # Podem escollir tenir nomes una entrada a un dels costat i crear un coll d'ampolla
        #             else: fila = m-1
        #         else: fila = random.choice(posibles_files)

        #         if not parets: return entrades, passadis

        #         posibles_entradas = ([p for p in parets if p[0] == fila])
        #         if posibles_entradas:
        #             p = random.choice(posibles_entradas)
        #         else: continue

        #         entrada.append(p)
        #         if p in parets: parets.remove(p)
            
        #         if (p[1] + a_entrada-1) < (n-1) and (p[0], p[1]+a_entrada-1) in parets:
        #             for i in range(a_entrada - 1): 
        #                 entrada.append((p[0], p[1]+i+1))
        #                 if p in parets: parets.remove((p[0], p[1]+i+1))

        #         elif (p[1] - a_entrada-1) > 0 and (p[0], p[1]-a_entrada+1) in parets:
        #             for i in range(a_entrada - 1): 
        #                 entrada.append((p[0], p[1]-i-1))
        #                 if p in parets: parets.remove((p[0], p[1]-i-1))

        #         elif (p[0] + a_entrada-1) < (m-1) and (p[0]+a_entrada-1, p[1]) in parets:
        #             for i in range(a_entrada - 1): 
        #                 entrada.append((p[0]+i+1, p[1]))
        #                 if p in parets: parets.remove((p[0]+i+1, p[1]))

        #         elif (p[0] - a_entrada-1) > 0 and (p[0]-a_entrada+1, p[1]) in parets:
        #             for i in range(a_entrada - 1): 
        #                 entrada.append((p[0]-i-1, p[1]))
        #                 if p in parets: parets.remove((p[0]-i-1, p[1]))

        #         else: 
        #             if a_entrada == 1: entrades.append(entrada)
        #             else: entrada.remove(p)

        #         if entrada: entrades.append(entrada)
    
    # elif mod == 'coll_ampolla':
    #     entrades.append([p for p in parets if p[0] == (m-1)])

    #     entrada = []
    #     for j in range(3):
    #         entrada.append((0, int((n/2) + j - 1)))
        
    #     entrades.append(entrada)
    
    # for entrada in entrades:
    #     for e in entrada:
    #         passadis[e] = 3

    return entrades, passadis