import numpy as np
import matplotlib.pyplot as plt

class Individuo:
    def __init__(self, posicion):
        self.posicion = posicion          # dupla (x, y) que dona la posicio en el passadis
        #self.velocitat = velocitat     # pot prendre valors: 0.25, 0.5, 0.75, 1
        #self.camp_visio = camp_visio   # dupla de enters (i, j) que indica la distància (en quadrats) màxima a la que pot veure l'individu dins del mapa. i mira la fila, j la columna. El camp de visió no es pot modificar un cop establert
        #self.objetivo = objetivo       # dupla (x, y) amb la posició a la que vol arribar l'individu       

    def get_posicion(self):
        return self.posicion
    
    def set_posicion(self, nova_posicion):
        self.posicion = nova_posicion
    
    # def get_velocitat(self):
    #     return self.velocitat

    # def set_velocitat(self, nova_velocitat):
    #     self.velocitat = nova_velocitat

    # def avançar(self):
    #   Definir diferents tipus de moviment
    #   set_posicio(...)

# Definir el tamaño de la malla
m = 8
n = 4

# Crear la malla
grid = np.zeros((m, n))

# Les entrades dels carrils que van en direcció cap a dalt son de la forma (m-1, j) 0 <= j <= n
# Les sortides dels carrils que van en direcció cap a dalt son de la forma (0, j) 0 <= j <= n

# Les entrades dels carrils que van en direcció cap a baix son de la forma (0, j) 0 <= j <= n
# Les sortides dels carrils que van en direcció cap a baix son de la forma (m-1, j) 0 <= j <= n

# Si j és parell la direcció serà cap a dalt i si és senar cap a baix
entradas = []
salidas = []
for j in range(n):
    if j % 2 == 0:
        entradas.append((m-1, j))
        salidas.append((0, j))
    else:
        entradas.append((0, j))
        salidas.append((m-1, j))

# Añadimos los individuos a la figura
individuos = []

# Definimos el número de iteraciones
num_iteraciones = m

# Simulamos el movimiento de los individuos en cada iteración
for t in range(num_iteraciones):

    # SE TIENE QUE REVISAR LA CREACIÓN DE INDIVIDUOS
    # if t % 2 == 0:
    if t == 0:
        # Creamos individuos nuevos y los añadimos a la lista
        for j in range(n):
            individuos.append(Individuo(entradas[j]))
            grid[individuos[j].get_posicion()] = 1

    # Configuramos el tamaño de los cuadrados de la malla
    plt.xticks(np.arange(0, n+1, 1))
    plt.yticks(np.arange(0, m+1, 1))

    # Agregamos los bordes negros
    for i in range(m+1):
        if i < (n+1):
            plt.axvline(i, color='black', lw=2)
        plt.axhline(i, color='black', lw=2)

    # Iteramos sobre los carriles
    for j in range(n):
        # Si j es par, la dirección es hacia arriba
        if j % 2 == 0:
            # Añadimos la entrada
            plt.scatter(j+0.5, 0.5, marker='^', s=150, color='green')
            # Añadimos la salida
            plt.scatter(j+0.5, m-1+0.5, marker='^', s=150, color='red')

        # Si j es impar, la dirección es hacia abajo
        else:
            # Añadimos la entrada
            plt.scatter(j+0.5, m-1+0.5, marker='v', s=150, color='green')
            # Añadimos la salida
            plt.scatter(j+0.5, 0.5, marker='v', s=150, color='red')

    # Dibujamos la malla en el tiempo t
    plt.imshow(grid, cmap='gray_r', extent=[0, n, 0, m], vmin=0, vmax=1, alpha=0.5)

    # Actualizamos la figura
    plt.title('Tiempo: ' + str(t))
    plt.pause(1)
    plt.clf()

    print(grid)

    # Movemos a cada individuo
    for individuo in individuos:
        i, j = individuo.get_posicion()
        grid[i, j] = 0 # Borramos la posición anterior

        
        # Movemos los individuos en el carril 1 a no ser que esten en la última fila
        if j % 2 == 0 and i != 0:
            i -= 1
        # Movemos los individuos en el carril 2 a no ser que esten en la última fila
        if j % 2 == 1 and i != m-1:
            i += 1

        individuo.set_posicion((i,j)) # Actualizamos la posición del individuo
        grid[i, j] = 1 # Añadimos al individuo en la nueva posición

