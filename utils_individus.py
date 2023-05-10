import numpy as np
import random
from scipy.optimize import linprog


# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(entrada, entrades):
    posibles_sortides = [sortida for sortida in entrades if sortida[0] != entrada[0] and sortida != entrada] # Afegir avaluació de la fila
    return random.choice(posibles_sortides)


# Calcula la velocitat màxima que podrà tenir un individu
def calcul_velocitat():
    velocitats = [0.25, 0.5, 0.75, 1]
    probabilitats = [0.15, 0.25, 0.35, 0.25]

    # La funció np.random.choice pren com a argument la llista de valors possibles (velocitats) i la distribució discreta de probabilitats 
    # corresponent (probabilitats). L'argument p indica les probabilitats corresponents a cada valor de la llista.
    velocitat = np.random.choice(velocitats, p=probabilitats)
    
    return velocitat


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

            v_rel = np.array(ind_a.get_velocitat()) - np.array(ind_b.get_velocitat())
            p_rel = np.array(ind_a.get_posicio()) - np.array(ind_b.get_posicio())
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


def calcular_velocitat_optima(individu, restricciones):
    velocitat_preferida = individu.get_velocitat_preferida()
    velocitat_actual = individu.get_velocitat()

    # Funció objetiu: minimitzar la desviació de la velocitat preferida i la velocitat actual
    c = [velocitat_actual[0] - velocitat_preferida[0], velocitat_actual[1] - velocitat_preferida[1]]

    # Construir les matrius de restriccions i límits
    A = []
    b = []

    for restriccio in restriccions[individu.get_id()]:
        p_tang, u = restriccio
        A.append(u)
        b.append(np.dot(u, p_tang))

    # Límits per les variables de velocitat (límits inferiors i superiors)
    bounds = [(-individu.get_velocitat_preferida(), individu.get_velocitat_preferida()),
              (-individu.get_velocitat_preferida(), individu.get_velocitat_preferida())]

    # Resoldre el problema d'optimizació lineal
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)

    # Extraure la velocitat optima de la solució
    v_optima = res.x

    return v_optima


def actualitzar_posicions_velocitats(individus, restriccions, dt):
    for ind in individus:
        # Calcular la velocitat optima per a l'individu
        v_optima = calcular_velocitat_optima(ind, restriccions)

        # Actualitzar la velocitat de l'individu
        ind.set_velocitat(v_optima)

        # Calcular la nova posició de l'individu utilitzant la velocitat optima i l'interval de temps dt
        nova_posicio = np.array(ind.get_posicio()) + (v_optima * dt)

        # Actualizar la posición del individuo
        ind.set_posicio(tuple(nova_posicio))












# def calcular_velocitat_optima(individu, restricciones):
#     velocitat_preferida = individu.get_velocitat_preferida()
#     velocitat_actual = individu.get_velocitat()
#     v_optima = velocitat_actual
#     min_penalizacion = float('inf')

#     for restriccion in restricciones.values():
#         t_col, p_tang, u_perp = restriccion['t_col'], restriccion['p_tang'], restriccion['u_perp']
#         v_candidata = p_tang + (t_col * u_perp)

#         # Normalizar la velocidad candidata si supera la velocidad preferida
#         if np.linalg.norm(v_candidata) > velocitat_preferida:
#             v_candidata = (v_candidata / np.linalg.norm(v_candidata)) * velocitat_preferida

#         # Calcular la penalización de la velocidad candidata
#         penalizacion = np.linalg.norm(v_candidata - velocitat_actual) + np.linalg.norm(v_candidata - individu.get_velocitat_preferida())

#         # Actualizar la velocidad óptima si la penalización es menor que la penalización mínima actual
#         if penalizacion < min_penalizacion:
#             min_penalizacion = penalizacion
#             v_optima = v_candidata

#     return v_optima


# def actualitzar_individus(individus, restriccions, dt):
#     for ind in individus:
#         v_optima = calcular_velocitat_optima(ind, restriccions[ind.get_id()])
#         ind.set_velocitat(v_optima)
#         nova_posicion = np.array(ind.get_posicio()) + (v_optima * dt)
#         ind.set_posicio(tuple(nova_posicion))


# def moure_individu(individu, passadis):
#     x, y = individu.get_posicio()
#     objectiu = individu.get_objectiu()
#     matriu = passadis.get_passadis()

#     if((x,y) == objectiu):
#         individu.set_posicio(None)
#         passadis.ind_in_passadis.remove(individu)
#         return
    
#     # Obtenim les posicions vàlides adjacents a la posició actual
#     posicions_valides = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y+1), (x+1, y+1), (x-1, y-1), (x+1, y-1)]
#     posicions_valides = [pos for pos in posicions_valides if 0 <= pos[0] < passadis.get_m() and 0 <= pos[1] < passadis.get_n() and matriu[pos] != 2 and matriu[pos] != 1]

#     if not posicions_valides:
#         return

#     # Calculem la distància euclidiana entre les posicions vàlides i l'objectiu
#     distancies = [((pos[0] - objectiu[0])**2 + (pos[1] - objectiu[1])**2)**0.5 for pos in posicions_valides]

#     # Seleccionem la direcció amb la distància més curta a l'objectiu
#     direccio_escollida = posicions_valides[np.argmin(distancies)]

#     # Si la direcció escollida és una entrada/sortida, l'individu arriba al seu objectiu i eliminem la seva posició
#     if direccio_escollida in passadis.get_entrades() and individu.get_objectiu() == direccio_escollida:
#         individu.set_posicio(direccio_escollida)
#         matriu[x, y] = 0
#     else:
#         # Actualitzem la posició de l'individu i la matriu
#         matriu[x, y] = 0
#         matriu[direccio_escollida] = 1
#         individu.set_posicio(direccio_escollida)