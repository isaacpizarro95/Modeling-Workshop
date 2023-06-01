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
    entrades = passadis.get_entrades()

    for x,y in parets:
        if(x,y) in passadis.get_parets():
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='gray', alpha=0.5)) #Parets
        
        else:
            plt.gca().add_patch(plt.Rectangle((y, m-x-1), 1, 1, color='black')) #Cantonades

        if (x,y) in entrades:
            if passadis.get_entrada_unica() == True:
                if x == 0: color = 'blue'
                else: color = 'green'
            else:
                colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
                color = colors[passadis.entrades.index((x,y)) % len(colors)]
            plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=200, color=color)

    # Dibuixem els individus amb els colors corresponents
    for ind in individus:
        if ind.posicio == None: continue

        entrada = ind.get_recorregut()[0]
        if passadis.get_entrada_unica() == True:
            if entrada[0] == 0: color = 'blue'
            else: color = 'green'
        else:
            colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'yellow']
            color = colors[passadis.entrades.index(entrada) % len(colors)] # Calculem el color que li toca al individu a partir de la seva entrada
        x, y = ind.get_posicio()
        plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=100, color=color) # Pintem el color de l'individu en la posició que es troba


    # Ajustem els eixos per adaptar-los a la mida de la finestra
    plt.axis('scaled')
    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #plt.get_current_fig_manager().full_screen_toggle()

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    plt.pause(0.35)
    plt.clf()