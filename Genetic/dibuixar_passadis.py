import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, passadis, individus, t):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    # Pintem les vores de color blanc per diferenciar els quadrats
    # for i in range(m+1):
    #     if i < (n+1):
    #         plt.axvline(i, color='white', lw=2)
    #     plt.axhline(i, color='white', lw=2)

    parets = passadis.get_parets()
    parets.extend([(0,0), (0,n-1), (m-1,0), (m-1,n-1)])
    vector_entrades = passadis.get_entrades()
    entrades = [e for entrada in vector_entrades for e in entrada]
    obstacles = passadis.get_obstacles()
    
    for x,y in obstacles:
        plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black'))

    for x,y in parets:
        if(x,y) in passadis.get_parets():
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

        objectiu = ind.get_objectiu()
        x, y = ind.get_posicio()
        dx, dy = ind.get_direccio()

        for entrada in vector_entrades:
            if objectiu in entrada:
                colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                color = colors[vector_entrades.index(entrada) % len(colors)]

                cercle = plt.Circle((y+0.5, m-x-1+0.5), radius=0.1, color=color)
                plt.gca().add_patch(cercle)
                direccio = mpatches.FancyArrow(y+0.5, m-x-1+0.5, 0.1*dy, -0.1*dx, width=0.05, color=color)
                plt.gca().add_patch(direccio)

    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    plt.pause(0.5)
    plt.clf()