import matplotlib.pyplot as plt
import numpy as np

# DIFERENCIAMOS 

# Para diferenciar gráficamente a los individuos, una posible opción es asignarles colores diferentes. 
# Puedes crear una lista de colores y asignar uno a cada individuo según su identificador. 
# Por ejemplo, podrías crear una lista de colores RGB aleatorios utilizando la biblioteca random de Python y la función randint() 
# para generar valores aleatorios para cada canal de color.

# Luego, puedes utilizar estos colores para dibujar cada punto correspondiente a un individuo en el gráfico. 
# Donde colors es la lista de colores generada anteriormente, y ind.id % len(colors) se utiliza para obtener el índice correspondiente 
# al color en la lista para cada individuo. De esta forma, se asegura que cada individuo tenga un color diferente, independientemente de 
# su identificador.

# Funció per dibuixar el passadís
def dibuixar_passadis(n, m, matriu, individus, t):
    # Configurem el tamany dels quadrats del passadís
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    # Pintem les vores de color negre per diferenciar els quadrats
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='black', lw=2)
        plt.axhline(i, color='black', lw=2)

    # Iterem sobre els carrils
    for j in range(n):
        # Si j és parell, la direcció és "cap a dalt"
        if j % 2 == 0:
            # Afegim el símbol de entrada
            plt.scatter(j+0.5, 0.5, marker='^', s=150, color='green')
            # Afegim el símbol de sortida
            plt.scatter(j+0.5, m-1+0.5, marker='^', s=150, color='red')

        # Si j és senar, la direcció és "cap a baix"
        else:
            # Afegim el símbol de entrada
            plt.scatter(j+0.5, m-1+0.5, marker='v', s=150, color='green')
            # Afegim el símbol de sortida
            plt.scatter(j+0.5, 0.5, marker='v', s=150, color='red')

    # Dibuixem els individus amb els colors corresponents
    for ind in individus:
        if ind.posicio is not None:
            x, y = ind.get_posicio()
            colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink']
            color = colors[ind.id % len(colors)] # Calculem el color que li toca al individu a partir del seu id
            plt.scatter(y+0.5, m-x-1+0.5, marker='o', s=100, color=color) # Pintem el color de l'individu en la posició que es troba
    # Dibuixem el passadís amb una escala de grisos que va del 0 al 1. Si el quadrat val 0 serà blanc i si val 1 serà el màxim fosc que permetem
    plt.imshow(matriu, cmap='gray_r', extent=[0, n, 0, m], vmin=0, vmax=1, alpha=0.5) # alpha dona transparència per a que no sigui tant fosc

    # Actualitzem la figura del passadís en cada unitat de temps 't'
    plt.title('Temps: ' + str(t))
    plt.pause(1)
    plt.clf()