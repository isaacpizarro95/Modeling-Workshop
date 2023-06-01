import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

class Individuo:
    def __init__(self, id, posicio, velocitat, radi, temps_horitzo):
        self.id = id
        self.posicio = posicio
        self.velocitat = velocitat
        self.radi = radi
        self.temps_horitzo = temps_horitzo

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio

    def get_velocitat(self):
        return self.velocitat

    def get_radi(self):
        return self.radi

    def get_temps_horitzo(self):
        return self.temps_horitzo

# Calcula les restriccions dels individus
def calcular_restricciones(individuos):
    restricciones = {}

    # Pas 1: Inicialitzar les restriccions de velocitat para cada individu
    for ind in individuos:
        restricciones[ind.get_id()] = []

    # Pas 2: Calcular les restriccions de velocitat imposades per altres individus
    for i in range(len(individuos)):
        ind_a = individuos[i]

        for j in range(i+1, len(individuos)):
            ind_b = individuos[j]

            v_rel = np.array(ind_b.get_velocitat()) - np.array(ind_a.get_velocitat())
            if np.all(v_rel == 0): continue
            p_rel = np.array(ind_b.get_posicio()) - np.array(ind_a.get_posicio())
            dist = np.linalg.norm(p_rel)
            t_col = (dist - ind_a.get_radi() - ind_b.get_radi()) / np.linalg.norm(v_rel)

            if t_col < ind_a.get_temps_horitzo():
                u = p_rel / dist # vector en la direcció de la posició relativa dels dos agents
                p_mid = (ind_a.get_radi() * u) + 0.5 * (dist - ind_a.get_radi() - ind_b.get_radi()) * u # punt mig entre els dos agents en el limit dels seus radis
                u_perp = np.array([-u[1], u[0]]) # vector perpendicular a u
                p_tang = p_mid - (ind_a.get_radi() * u_perp) # punt tangent en el limit del radi del individu a

                restriccion = (p_tang, u)
                restricciones[ind_a.get_id()].append(restriccion)
                restricciones[ind_b.get_id()].append(restriccion)

    return restricciones

# Crear algunos individuos
individuo1 = Individuo(id=1, posicio=(0, 0), velocitat=(1, 1), radi=1, temps_horitzo=10)
individuo2 = Individuo(id=2, posicio=(-2, 4), velocitat=(-1, -1), radi=1, temps_horitzo=10)
individuo3 = Individuo(id=3, posicio=(4, 3), velocitat=(1, -1), radi=1, temps_horitzo=10)
individuo4 = Individuo(id=4, posicio=(-3, -2), velocitat=(0, 2), radi=1, temps_horitzo=10)
individuo5 = Individuo(id=5, posicio=(8, 4), velocitat=(1, -2), radi=1, temps_horitzo=10)

# p_rel = np.array(individuo1.get_posicio()) - np.array(individuo2.get_posicio())
# dist = np.linalg.norm(p_rel)
# u = p_rel / dist
# u_perp = np.array([-u[1], u[0]])
# p_mid = (individuo1.get_radi() * u) + 0.5 * (dist - individuo1.get_radi() - individuo2.get_radi()) * u
# p_tang = p_mid - (individuo1.get_radi() * u_perp)
# print(f"Restricció individu 1 i 2:\nPosició relativa = {p_rel}\nDistància = {dist}\nu = {u}\nu perpendicular = {u_perp}\nPunt mig entre els radis = {p_mid}\nPunt tangent = {p_tang}")

individuos = [individuo1, individuo2, individuo3, individuo4]#, individuo3, individuo4, individuo5]

# Calcular las restricciones
restricciones = calcular_restricciones(individuos)

fig, ax = plt.subplots()

# Definir colores para los individuos
colores = ['red', 'blue', 'green', 'purple', 'yellow']  # Asegúrate de tener suficientes colores para todos los individuos

# Dibujar posiciones de los individuos y velocidades
for i, ind in enumerate(individuos):
    circle = plt.Circle(ind.get_posicio(), ind.get_radi(), fill=True, facecolor=colores[i], edgecolor=colores[i])
    ax.add_artist(circle)
    circle = plt.Circle(ind.get_posicio(), ind.get_radi(), fill=False)
    ax.add_artist(circle)

    ax.text(ind.get_posicio()[0], ind.get_posicio()[1], str(ind.get_id()), fontsize=12, ha='center')

    # Dibujar velocidad
    vel = ind.get_velocitat()
    ax.quiver(ind.get_posicio()[0], ind.get_posicio()[1], vel[0], vel[1], angles='xy', scale_units='xy', scale=1, color=colores[i])

# # Agregar los vectores perpendiculares al gráfico con los colores correspondientes
# for i, restriccion in enumerate(restricciones[1]):
#     p_tang, u = restriccion
#     u_perp = np.array([-u[1], u[0]])
#     color = colores[(i+1) % len(colores)]  # Usa el color correspondiente al individuo
#     plt.quiver(p_tang[0], p_tang[1], u_perp[0], u_perp[1], angles='xy', scale_units='xy', scale=1, color=color)
for i, restriccion in enumerate(restricciones[1]):
    p_tang, u = restriccion
    u_perp = np.array([-u[1], u[0]])
    color = colores[(i+1) % len(colores)]  # Usa el color correspondiente al individuo

    # Dibuja el vector perpendicular
    plt.quiver(p_tang[0], p_tang[1], u_perp[0], u_perp[1], angles='xy', scale_units='xy', scale=1, color=color)

    # Dibuja la línea que pasa por el punto de tangencia y tiene la dirección del vector perpendicular
    t_values = np.linspace(-10, 10, 100)  # Ajusta los valores de 't' según sea necesario
    line_points = [p_tang + t * u_perp for t in t_values]
    x_values, y_values = zip(*line_points)
    plt.plot(x_values, y_values, color=color)

# 1. Encuentra las intersecciones
intersecciones = []
for i in range(len(restricciones[1])):
    for j in range(i + 1, len(restricciones[1])):
        interseccion = encuentra_interseccion(restricciones[1][i], restricciones[1][j])
        if interseccion is not None:
            intersecciones.append(interseccion)

# 2. Filtra las intersecciones válidas
intersecciones_validas = []
for interseccion in intersecciones:
    if es_valida(interseccion, restricciones[1]):
        intersecciones_validas.append(interseccion)

# 3. Dibuja y rellena el polígono
x_values, y_values = zip(*intersecciones_validas)
plt.fill(x_values, y_values, 'b', alpha=0.3)  # Cambia 'b' y alpha=0.3 a los valores que prefieras



# Ordenamos los puntos de tangencia alrededor del centro del individuo 1
restricciones[1].sort(key=lambda restriccion: np.arctan2(restriccion[0][1] - individuo1.get_posicio()[1], restriccion[0][0] - individuo1.get_posicio()[0]))

# Obtenemos los puntos de tangencia
puntos_tangencia = [restriccion[0] for restriccion in restricciones[1]]

plt.xlim(-6, 6)
plt.ylim(-6, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()




# # Verificamos que haya al menos 3 puntos para formar un polígono
# if len(puntos_tangencia) >= 3:
#     # Calculamos el convex hull
#     hull = ConvexHull(puntos_tangencia)
#     # Obtenemos los puntos del convex hull
#     puntos_hull = [puntos_tangencia[i] for i in hull.vertices]
#     # Creamos el polígono
#     poligono = Polygon(puntos_hull)

#     # Dibujamos el polígono
#     #patch = patches.Polygon(np.array(poligono.exterior), closed=True, alpha=0.3, color='green')
#     patch = patches.Polygon(np.array(poligono.exterior.coords), closed=True, alpha=0.3, color='green')
#     ax.add_patch(patch)

# # Agregamos una declaración de impresión para ver las restricciones
# print("Restricciones:", restricciones[1])

# # Calculamos y dibujamos el polígono de la región alcanzable
# poligono = Polygon([restriccion[0] for restriccion in restricciones[1]])

# # Agregamos una declaración de impresión para ver los puntos de tangencia
# print("Puntos de tangencia:", [restriccion[0] for restriccion in restricciones[1]])

# if not poligono.is_empty:  # Comprobamos si el polígono tiene puntos en su contorno exterior
#     patch = patches.Polygon(np.array(poligono.exterior), closed=True, alpha=0.3, color='green')
#     ax.add_patch(patch)

# plt.xlim(-10, 10)
# plt.ylim(-10, 10)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()


# # Dibujar restricciones del individuo 1
# for r in restricciones[individuo1.get_id()]:
#     p_tang, u = r
#     ax.arrow(*p_tang, *u, color='r')

# # Calcular región disponible para el individuo 1
# lineas = [LineString([(x[0][0] - 1000 * x[1][0], x[0][1] - 1000 * x[1][1]), 
#                       (x[0][0] + 1000 * x[1][0], x[0][1] + 1000 * x[1][1])]) 
#           for x in restricciones[individuo1.get_id()]]

# union = unary_union(lineas)
# intersecciones = list(polygonize(union))

# for poligono in intersecciones:
#     if poligono.exterior is not None:
#         patch = patches.Polygon(np.array(poligono.exterior), closed=True, alpha=0.3, color='green')
#         ax.add_patch(patch)

# ax.set_xlim(-5, 5)
# ax.set_ylim(-5, 5)
# plt.grid(True)
# plt.show()