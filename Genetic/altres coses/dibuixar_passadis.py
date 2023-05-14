import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, parets, vector_entrades, individus):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    #Pintem les vores de color blanc per diferenciar els quadrats
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='white', lw=2)
        plt.axhline(i, color='white', lw=2)

    parets.extend([(0,0), (0,n-1), (m-1,0), (m-1,n-1)])
    entrades = [e for entrada in vector_entrades for e in entrada]

    for x,y in parets:
        if(x,y) in parets:
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.5)) #Parets
        
        else:
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black')) #Cantonades

        if (x,y) in entrades:
            for entrada in vector_entrades:
                if (x,y) in entrada:
                    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                    color = colors[vector_entrades.index(entrada) % len(colors)]
            plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=200, color=color)

    # Dibuixem els individus amb els colors corresponents
    for ind in individus:
        if ind.posicio == None: continue

        x, y = ind.get_posicio()
        dx, dy = ind.get_direccio()

        for entrada in vector_entrades:
            #colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
            color = 'black'
            if individus.index(ind) == 0:
                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color='brown')
                plt.gca().add_patch(cercle)
            else:
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color=color)
                plt.gca().add_patch(direccio)

    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.pause(100.0)
    plt.clf()

class Individu():
    def __init__(self, posicio, direccio):
        self.posicio = posicio
        self.direccio = direccio
    
    def get_posicio(self):
        return self.posicio
    
    def get_direccio(self):
        return self.direccio

m = 15
n = 11
matriu = np.zeros((m, n))
parets = []
for i in range(m):
    for j in range(n):
        if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
            if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
                matriu[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
            else:
                matriu[i, j] = 2  # Perímetre
                parets.append((i, j))
entrades = []
entrades.append([p for p in parets if p[0] == 0])
entrades.append([p for p in parets if p[0] == (m-1)])
for entrada in entrades:
    for e in entrada:
        matriu[e] = 3

individus = []
# Punt central
individus.append(Individu((7, 5), (0, 0)))
# # Grup 1
# individus.append(Individu((6, 4), (-1, -1)))
# individus.append(Individu((5, 4), (-1, -1)))
# individus.append(Individu((4, 4), (-1, -1)))
# individus.append(Individu((6, 3), (-1, -1)))
# individus.append(Individu((5, 3), (-1, -1)))
# individus.append(Individu((4, 3), (-1, -1)))
# individus.append(Individu((6, 2), (-1, -1)))
# individus.append(Individu((5, 2), (-1, -1)))
# individus.append(Individu((4, 2), (-1, -1)))
# # Grup 2
# individus.append(Individu((6, 6), (-1, 1)))
# individus.append(Individu((5, 6), (-1, 1)))
# individus.append(Individu((4, 6), (-1, 1)))
# individus.append(Individu((6, 7), (-1, 1)))
# individus.append(Individu((5, 7), (-1, 1)))
# individus.append(Individu((4, 7), (-1, 1)))
# individus.append(Individu((6, 8), (-1, 1)))
# individus.append(Individu((5, 8), (-1, 1)))
# individus.append(Individu((4, 8), (-1, 1)))
# # Grup 3
# individus.append(Individu((8, 4), (1, -1)))
# individus.append(Individu((9, 4), (1, -1)))
# individus.append(Individu((10, 4), (1, -1)))
# individus.append(Individu((8, 3), (1, -1)))
# individus.append(Individu((9, 3), (1, -1)))
# individus.append(Individu((10, 3), (1, -1)))
# individus.append(Individu((8, 2), (1, -1)))
# individus.append(Individu((9, 2), (1, -1)))
# individus.append(Individu((10, 2), (1, -1)))
# # Grup 4
# individus.append(Individu((8, 6), (1, 1)))
# individus.append(Individu((9, 6), (1, 1)))
# individus.append(Individu((10, 6), (1, 1)))
# individus.append(Individu((8, 7), (1, 1)))
# individus.append(Individu((9, 7), (1, 1)))
# individus.append(Individu((10, 7), (1, 1)))
# individus.append(Individu((8, 8), (1, 1)))
# individus.append(Individu((9, 8), (1, 1)))
# individus.append(Individu((10, 8), (1, 1)))
# Grup 5
individus.append(Individu((6, 5), (-1, 0)))
individus.append(Individu((5, 4), (-1, 0)))
individus.append(Individu((5, 5), (-1, 0)))
individus.append(Individu((5, 6), (-1, 0)))
individus.append(Individu((4, 3), (-1, 0)))
individus.append(Individu((4, 4), (-1, 0)))
individus.append(Individu((4, 5), (-1, 0)))
individus.append(Individu((4, 6), (-1, 0)))
individus.append(Individu((4, 7), (-1, 0)))
# Grup 6
individus.append(Individu((7, 4), (0, -1)))
individus.append(Individu((6, 3), (0, -1)))
individus.append(Individu((7, 3), (0, -1)))
individus.append(Individu((8, 3), (0, -1)))
individus.append(Individu((5, 2), (0, -1)))
individus.append(Individu((6, 2), (0, -1)))
individus.append(Individu((7, 2), (0, -1)))
individus.append(Individu((8, 2), (0, -1)))
individus.append(Individu((9, 2), (0, -1)))
# Grup 7
individus.append(Individu((8, 5), (1, 0)))
individus.append(Individu((9, 4), (1, 0)))
individus.append(Individu((9, 5), (1, 0)))
individus.append(Individu((9, 6), (1, 0)))
individus.append(Individu((10, 3), (1, 0)))
individus.append(Individu((10, 4), (1, 0)))
individus.append(Individu((10, 5), (1, 0)))
individus.append(Individu((10, 6), (1, 0)))
individus.append(Individu((10, 7), (1, 0)))
# Grup 8
individus.append(Individu((7, 6), (0, 1)))
individus.append(Individu((6, 7), (0, 1)))
individus.append(Individu((7, 7), (0, 1)))
individus.append(Individu((8, 7), (0, 1)))
individus.append(Individu((5, 8), (0, 1)))
individus.append(Individu((6, 8), (0, 1)))
individus.append(Individu((7, 8), (0, 1)))
individus.append(Individu((8, 8), (0, 1)))
individus.append(Individu((9, 8), (0, 1)))

dibuixar_passadis(n, m, parets, entrades, individus)