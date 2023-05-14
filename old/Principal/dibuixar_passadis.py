import matplotlib.pyplot as plt
import numpy as np

# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, passadis, individus, t):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    # Pintem les vores de color negre per diferenciar els quadrats
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='white', lw=2)
        plt.axhline(i, color='white', lw=2)

    parets = passadis.get_parets()
    parets.extend([(0,0), (0,n-1), (m-1,0), (m-1,n-1)])
    vector_entrades = passadis.get_entrades()
    entrades = [e for entrada in vector_entrades for e in entrada]

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
        inici = ind.get_recorregut()[0]

        for entrada in vector_entrades:
            if inici in entrada:
                colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                color = colors[vector_entrades.index(entrada) % len(colors)]
        x, y = ind.get_posicio()
        #if(ind.id == 1): plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=350, color=color) # Util si volem seguir a un en concret
        plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=100, color=color) # Pintem el color de l'individu en la posició que es troba


    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #plt.get_current_fig_manager().full_screen_toggle()

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    if m <= 30: plt.pause(0.75)
    elif 30 < m < 50: plt.pause(0.05)
    else: plt.pause(0.01)
    plt.clf()