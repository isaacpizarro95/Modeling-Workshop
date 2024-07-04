import numpy as np

# En el nostre passadís hi han 4 valors diferents:
# 0 si no hi ha individus ni obstacles
# 1 si hi ha un individu
# 2 si és una paret
# 3 si és una entrada/sortida (aquestes només poden apareixer a les parets)
# 4 si és un obstacle

def crear_passadis(m, n, a_entrada, num_entrades, entrada_unica, entrades_laterals, obstacles):
    """
    Funció per a crear un passadís.

    Paràmetres:
    m: nombre de files del passadís.
    n: nombre de columnes del passadís.
    a_entrada: amplada de l'entrada.
    num_entrades: nombre d'entrades al passadís.
    entrada_unica: si és True, tota la part superior i inferior del passadís serà entrada.
    entrades_laterals: si és True, hi hauran entrades a les parets laterals del passadís.
    obstacles: si és True, es crearan obstacles al passadís.
    """

    # Creem una matriu de zeros de m files i n columnes
    passadis = np.zeros((m, n))

    # Creem una llista buida per a guardar les posicions de les parets
    parets = []  

    # Recorrem cada cel·la de la matriu
    for i in range(m):
        for j in range(n):
            # Si la cel·la està en el perímetre de la matriu
            if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
                # Si la cel·la està en una cantonada de la matriu, la tractem com a obstacle
                if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                    passadis[i, j] = 4  
                else:
                    # Si la cel·la està en el perímetre però no en una cantonada, la tractem com a paret
                    passadis[i, j] = 2  
                    parets.append((i, j))

    # Creem les entrades del passadís
    entrades, passadis = crear_entrades(m, n, passadis, parets, a_entrada, num_entrades, entrada_unica, entrades_laterals)

    # Si volem obstacles, creem un quadrat en mig del passadís que actuarà com a obstacle
    obs = []
    if obstacles == True:
        obs = [(int(m/2), int(n/2)), (int(m/2-1), int(n/2)), (int(m/2), int(n/2+1)), (int(m/2-1), int(n/2+1)), (int(m/2), int(n/2-1)), (int(m/2-1), int(n/2-1))]
        for ob in obs:
            passadis[ob] = 4

    # Retornem el passadís, les entrades, les parets i els obstacles
    return passadis, entrades, parets, obs



def crear_entrades(m, n, passadis, parets_original, a_entrada, num_entrades, entrada_unica, entrades_laterals):
    """
    Funció per a crear les entrades del passadís.

    Paràmetres:
    m: nombre de files del passadís.
    n: nombre de columnes del passadís.
    passadis: matriu que representa el passadís.
    parets_original: llista de tuples que representen les posicions de les parets.
    a_entrada: amplada de l'entrada.
    num_entrades: nombre d'entrades al passadís.
    entrada_unica: si és True, tota la part superior i inferior del passadís serà entrada.
    entrades_laterals: si és True, hi hauran entrades a les parets laterals del passadís.
    """

    # Creem una llista buida per a guardar les entrades
    entrades = []

    # Copiem la llista de parets
    parets = parets_original.copy()

    # Si no volem entrades laterals, eliminem les parets laterals de la llista de parets
    if entrades_laterals == False:
        parets = [p for p in parets if p[0] == 0 or p[0] == (m-1)]

    # Si volem una entrada única, tota la part superior i inferior del passadís serà entrada
    if entrada_unica == True:
        entrades.append([p for p in parets if p[0] == 0])
        entrades.append([p for p in parets if p[0] == (m-1)])
    else:
        # Si no volem una entrada única, creem diverses entrades
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

        # Afegim les entrades a la llista d'entrades
        entrades.append(entrada1)
        entrades.append(entrada2)
        entrades.append(entrada3)
        entrades.append(entrada4)

    # Retornem les entrades i el passadís
    return entrades, passadis












# def crear_passadis(m, n, mod, a_entrada, num_entrades, entrada_unica, entrades_laterals, obstacles):
#     # Creem una matriu de zeros de m files i n columnes (m serà la llargada del passadís i n els carrils)
#     passadis = np.zeros((m, n))

#     # Afegim "parets" al passadís.
#     parets = []
#     if mod == 'coll_ampolla':
#         for i in range(m):
#             for j in range(n):
#                 if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
#                     if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
#                         passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
#                     else:
#                         passadis[i, j] = 2  # Perímetre
#                         parets.append((i, j))
                
#                 if i == int(m/2) and j != int(n/3) and j != (int(n/3)+int(n/3)):#and j != int(n/2)-1 and j != int(n/2) and j != int(n/2)+1:
#                         passadis[i, j] = 2
#                         parets.append((i, j))                   
#     else:     
#         for i in range(m):
#             for j in range(n):
#                 if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
#                     if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
#                         passadis[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
#                     else:
#                         passadis[i, j] = 2  # Perímetre
#                         parets.append((i, j))

#     entrades, passadis = crear_entrades(m, n, passadis, parets, a_entrada, num_entrades, entrada_unica, entrades_laterals)


#     # Creem un nombre aleatori entre 2 i 6 (nombres arbitraris) d'obstacles
#     obs = []
#     if obstacles == True:
#         obs = [(int(m/2), int(n/2)), (int(m/2-1), int(n/2)), (int(m/2), int(n/2+1)), (int(m/2-1), int(n/2+1)), (int(m/2), int(n/2-1)), (int(m/2-1), int(n/2-1))]
#         for ob in obs:
#             passadis[ob] = 4
#     # if obstacles == True:
#     #     possibles_obstacles = [np.argwhere(passadis == 0)]
#     #     for i in range(random.randint(2,6)):
#     #         ob = tuple(random.choice(possibles_obstacles[0]))
#     #         passadis[ob] = 4
#     #         obs.append(ob)

#     return passadis, entrades, parets, obs

# # Les entrades i sortides son en si el mateix. Poden entrar i sortir individus per ella.
# def crear_entrades(m, n, passadis, parets_original, a_entrada, num_entrades, entrada_unica, entrades_laterals):
#     entrades = []
#     parets = parets_original.copy()

#     #if mod == 'defecte':
#     # Si entrades_laterals == False només hi hauran entrades a la part superior i inferior del passadís.
#     if entrades_laterals == False:
#         parets = [p for p in parets if p[0] == 0 or p[0] == (m-1)]

#     #posibles_files = [p[0] for p in parets]

#     # Si entrada_unica == True tota la part superior i tota la part inferior serà entrada/sortida.
#     if entrada_unica == True:
#         entrades.append([p for p in parets if p[0] == 0])
#         entrades.append([p for p in parets if p[0] == (m-1)])

#     else:
#         entrada1 = [] 
#         entrada2 = [] 
#         entrada3 = [] 
#         entrada4 = []
#         if entrades_laterals == True:
#             for i in range(a_entrada):
#                 entrada1.append((0, int(n/2) + i - 1))
#                 entrada2.append((m-1, int(n/2) + i - 1))
#                 entrada3.append((int(m/2) + i - 1, 0))
#                 entrada4.append((int(m/2) + i - 1, n-1))            
#         else:
#             for i in range(a_entrada):
#                 entrada1.append((m - 1, int((n-1)/3) + i - 1))
#                 entrada2.append((m - 1, int((n-1)/3) * 2 + i - 1))
#                 entrada3.append((0, int((n-1)/3) + i - 1))
#                 entrada4.append((0, int((n-1)/3) * 2 + i - 1))

#         entrades.append(entrada1)
#         entrades.append(entrada2)
#         entrades.append(entrada3)
#         entrades.append(entrada4)

#     return entrades, passadis


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

