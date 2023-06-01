import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, parets, vector_entrades, individus, obstacles):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    #Pintem les vores de color blanc per diferenciar els quadrats
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='grey', lw=2)
        plt.axhline(i, color='grey', lw=2)

    # parets.extend([(0,0), (0,n-1), (m-1,0), (m-1,n-1)])
    # entrades = [e for entrada in vector_entrades for e in entrada]

    # for x,y in parets:
    #     if(x,y) in parets:
    #         plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.5)) #Parets
        
    #     else:
    #         plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black')) #Cantonades

    #     if (x,y) in entrades:
    #         for entrada in vector_entrades:
    #             if (x,y) in entrada:
    #                 colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
    #                 color = colors[vector_entrades.index(entrada) % len(colors)]
    #         plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=200, color=color)

    # Dibuixem els individus amb els colors corresponents
    i = 0
    for ind in individus:
        if ind.posicio == None: continue
        if i < 6:
            x, y = ind.get_posicio()
            dx, dy = ind.get_direccio()

            #for entrada in vector_entrades:
                #colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
            if dx == -1:
                color = 'blue'
                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color=color)
                plt.gca().add_patch(cercle)
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color=color)
                plt.gca().add_patch(direccio)
            else:
                color = 'red'
                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color=color)
                plt.gca().add_patch(cercle)
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color=color)
                plt.gca().add_patch(direccio)
        else:
            x, y = ind.get_posicio()
            dx, dy = ind.get_direccio()

            #for entrada in vector_entrades:
                #colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
            if dx == -1:
                color = 'blue'
                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color=color)
                plt.gca().add_patch(cercle)
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color='red')
                plt.gca().add_patch(direccio)
            else:
                color = 'red'
                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color=color)
                plt.gca().add_patch(cercle)
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color='blue')
                plt.gca().add_patch(direccio)

        i += 1 
    
    #direccio = mpatches.FancyArrow(5+0.5, m-6-1+0.5, 0.1*0, -0.1*-1, width=0.05, color='black')
    #plt.gca().add_patch(direccio)
    # for pos in obstacles:
    #     x, y = pos
    #     plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.9))

    # Objectiu
    #plt.gca().add_patch(plt.Rectangle((3, m-0-1), 1, 1, color='black'))

    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.pause(20.0)
    plt.clf()

class Individu():
    def __init__(self, posicio, direccio):
        self.posicio = posicio
        self.direccio = direccio
    
    def get_posicio(self):
        return self.posicio
    
    def get_direccio(self):
        return self.direccio

m = 4
n = 3
matriu = np.zeros((m, n))
# parets = []
# for i in range(m):
#     for j in range(n):
#         if i == 0 or i == (m - 1) or j == 0 or j == (n - 1):
#             if (i, j) in [(0, 0), (0, n-1), (m-1, 0), (m-1, n-1)]:
#                 matriu[i, j] = 4  # Tractem les cantonades com a obstacles per a que no es puguin crear entrades
#             else:
#                 matriu[i, j] = 2  # Perímetre
#                 parets.append((i, j))
# entrades = []
# entrades.append([p for p in parets if p[0] == 0])
# entrades.append([p for p in parets if p[0] == (m-1)])
# entrades.append([(4,0),(5,0),(6,0)])
# entrades.append([(4,n-1),(5,n-1),(6,n-1)])
# for entrada in entrades:
#     for e in entrada:
#         matriu[e] = 3

# obstacles = [(4,2),(4,3),(4,4),(5,2),(5,3),(5,4),(6,2),(6,3),(6,4)]
individus = []
# Punt central
#individus.append(Individu((7, 5), (-1, 0)))

#posiciones = [(6,4),(6,5), (6,6), (7,4), (7,5), (7,6), (8,4), (8,6)]
#posiciones = [(6,5), (5,4), (5,5), (5,6), (4,3), (4,4), (4,5), (4,6), (4,7)]
#individus.append(Individu((6, 5), (-1, 0)))
individus.append(Individu((0, 0), (-1, 0)))
individus.append(Individu((0, 1), (-1, 0)))
individus.append(Individu((0, 2), (1, 0)))
individus.append(Individu((1, 0), (-1, 0)))
individus.append(Individu((1, 1), (-1, 0)))
individus.append(Individu((1, 2), (1, 0)))
individus.append(Individu((2, 0), (-1, 0)))
individus.append(Individu((2, 1), (1, 0)))
individus.append(Individu((2, 2), (-1, 0)))
individus.append(Individu((3, 0), (1, 0)))
individus.append(Individu((3, 1), (-1, 0)))
individus.append(Individu((3, 2), (-1, 0)))

parets = []
entrades = []
obstacles = []
dibuixar_passadis(n, m, parets, entrades, individus, obstacles)