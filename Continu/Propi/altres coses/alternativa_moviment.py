import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Calcula dos segments a partir de quatre punts d'inici i final
def calcul_punts_direccio(ind):
    v_max = np.array(ind.get_v_max())
    v_opt = np.array(ind.get_velocitat_optima())  # Obtenemos la velocidad óptima
    pos = np.array(ind.get_posicio())
    radi = ind.get_radi()

    # Normalizamos v_opt para que tenga magnitud 1
    v_opt_norm = v_opt / np.linalg.norm(v_opt)

    # Calculamos un vector que es perpendicular a v_opt y tiene longitud radi
    perp_vector = np.array([-v_opt_norm[1], v_opt_norm[0]]) * radi

    # Calculamos los puntos de inicio de los segmentos izquierdo y derecho
    left_start = pos - perp_vector
    right_start = pos + perp_vector

    # Calculamos los puntos finales de los segmentos izquierdo y derecho
    # usando v_max para la longitud de los segmentos
    left_end = left_start + v_max * v_opt_norm
    right_end = right_start + v_max * v_opt_norm

    # Ajustamos por el radio en la dirección y
    left_start[1] -= radi
    right_start[1] -= radi
    left_end[1] += radi
    right_end[1] += radi

    return [[left_start.tolist(), left_end.tolist()], [right_start.tolist(), right_end.tolist()]]


# # Calcula la circumferència que conté els possibles punts als que potencialment es pot moure l'individu en el seguent instant de temps
# def calcul_circumferencia(ind, n_punts = 100):
#     v_max = ind.get_v_max()
#     x, y = ind.get_posicio()
#     radi = ind.get_radi()

#     # Genera n_punts equiespaiats entre 0 i 2pi
#     thetas = np.linspace(0, 2*np.pi, n_punts)

#     # Calcula el radio de la circunferencia teniendo en cuenta el radio del individuo
#     circ_radi = np.linalg.norm(v_max) + radi

#     # Calcula les coordenadas x, y dels punts
#     x_punts = x + circ_radi * np.cos(thetas)
#     y_punts = y + circ_radi * np.sin(thetas)
    
#     # Retorna una llista on cada element de la llista es un parell (x,y) dels conjunts x_punts, y_punts
#     return list(zip(x_punts, y_punts))


def calcula_cuadrado_movimiento(pos, radi):
    # Extraer las coordenadas x e y del centro
    x_centro, y_centro = pos

    # Calcular las coordenadas de los cuatro vértices del cuadrado de movimiento
    superior_izquierdo = (x_centro - radi, y_centro + radi)
    superior_derecho = (x_centro + radi, y_centro + radi)
    inferior_izquierdo = (x_centro - radi, y_centro - radi)
    inferior_derecho = (x_centro + radi, y_centro - radi)

    # Devolver los vértices del cuadrado de movimiento
    return [superior_izquierdo, superior_derecho, inferior_izquierdo, inferior_derecho]


def divide_cuadrado_en_celdas(vertices, n):
    superior_izquierdo, superior_derecho, inferior_izquierdo, inferior_derecho = vertices
    
    # Calcular el tamaño de cada celda
    tamano_celda = (superior_derecho[0] - superior_izquierdo[0]) / np.sqrt(n)

    # Crear una lista para almacenar las celdas
    celdas = []

    # Generar las celdas
    for i in np.arange(inferior_izquierdo[0], inferior_derecho[0], tamano_celda):
        for j in np.arange(inferior_izquierdo[1], superior_izquierdo[1], tamano_celda):
            celda_inferior_izquierdo = (i, j)
            celda_superior_derecho = (i + tamano_celda, j + tamano_celda)
            celdas.append([celda_inferior_izquierdo, celda_superior_derecho])

    # Devolver la lista de celdas
    return celdas


def calcular_celdas_libres(individus, n):
    celdas_libres = {}

    for i in range(len(individus)):
        ind_a = individus[i]
        pos_a = np.array(ind_a.get_posicio())
        radi_moviment = ind_a.get_radi_moviment()

        # Calculamos el cuadrado de movimiento
        vertices = calcula_cuadrado_movimiento(pos_a, radi_moviment)

        # Convertimos las celdas en tuplas y las guardamos en un conjunto
        #celdas = set(map(tuple, divide_cuadrado_en_celdas(vertices, n)))
        celdas = divide_cuadrado_en_celdas(vertices, n)

        celdas_libres[ind_a] = celdas  # Inicialmente todas las celdas están libres, lo guardamos como conjunto
        for j in range(len(individus)):
            if individus[j] == ind_a: continue
            ind_b = individus[j]
            rectangle_b = ind_b.get_direccio_moviment()

            for segment in rectangle_b:
                for celda in celdas_libres[ind_a]:  # Aseguramos que las celdas se manejen como tuplas
                    if intersecta_segmento_celda(segment, celda):
                        celdas_libres[ind_a].remove(celda)

    return celdas_libres


def punto_en_celda(punto, celda):
    # Descomponemos los componentes del punto y la celda
    px, py = punto
    (cx_min, cy_min), (cx_max, cy_max) = celda
    
    # Comprobamos si el punto está dentro de los límites de la celda
    return cx_min <= px <= cx_max and cy_min <= py <= cy_max


def orientacion(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colineales
    elif val > 0:
        return 1  # sentido horario
    else:
        return 2  # sentido antihorario


# Función auxiliar para comprobar si el punto q está en el segmento pr
def esta_en_segmento(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

# Retorna true si els dos segments intersecten i false si no ho fan
def intersectan(segmento_a, segmento_b):
    p1, q1 = segmento_a
    p2, q2 = segmento_b

    # Orientaciones requeridas para los casos de intersección general y especial
    o1 = orientacion(p1, q1, p2)
    o2 = orientacion(p1, q1, q2)
    o3 = orientacion(p2, q2, p1)
    o4 = orientacion(p2, q2, q1)

    # Caso general
    if o1 != o2 and o3 != o4:
        return True
    # Casos especiales: los puntos p1, q1 y p2 son colineales y p2 está en el segmento p1q1
    if o1 == 0 and esta_en_segmento(p1, p2, q1):
        return True
    # Casos especiales: los puntos p1, q1 y q2 son colineales y q2 está en el segmento p1q1
    if o2 == 0 and esta_en_segmento(p1, q2, q1):
        return True
    # Casos especiales: los puntos p2, q2 y p1 son colineales y p1 está en el segmento p2q2
    if o3 == 0 and esta_en_segmento(p2, p1, q2):
        return True
    # Casos especiales: los puntos p2, q2 y q1 son colineales y q1 está en el segmento p2q2
    if o4 == 0 and esta_en_segmento(p2, q1, q2):
        return True

    return False  # No existe intersección


def intersecta_segmento_celda(segment, celda):
    A, B = segment
    
    if punto_en_celda(A, celda) or punto_en_celda(B, celda):
        return True
    
    C, D = celda[0], [celda[0][0], celda[1][1]]  # Lado izquierdo de la celda
    if intersectan((A, B), (C, D)):
        return True

    C, D = celda[0], [celda[1][0], celda[0][1]]  # Lado inferior de la celda
    if intersectan((A, B), (C, D)):
        return True

    C, D = celda[1], [celda[0][0], celda[1][1]]  # Lado derecho de la celda
    if intersectan((A, B), (C, D)):
        return True

    C, D = celda[1], [celda[1][0], celda[0][1]]  # Lado superior de la celda
    if intersectan((A, B), (C, D)):
        return True

    return False





def calcula_nueva_velocidad(individuo, celdas_libres):
    celdas = celdas_libres[individuo]
    v_max = individuo.get_v_max()
    pos = individuo.get_posicio()
    objectiu = individuo.get_objectiu()

    # Calcula la dirección a la meta
    direccion = np.array(objectiu) - np.array(pos)

    # Filtra las celdas libres que están en la dirección de la meta
    # celdas = [celda for celda in celdas if (
    #     ((celda[0][0] + celda[1][0]) / 2 >= pos[0] and direccion[0] > 0) or 
    #     ((celda[0][0] + celda[1][0]) / 2 <= pos[0] and direccion[0] < 0) or 
    #     ((celda[0][1] + celda[1][1]) / 2 >= pos[1] and direccion[1] > 0) or 
    #     ((celda[0][1] + celda[1][1]) / 2 <= pos[1] and direccion[1] < 0)
    # )]

    # Encuentra la celda libre más cercana al objetivo
    min_dist = float('inf')
    celda_optima = None
    for celda in celdas:
        centro_celda = [(celda[0][0] + celda[1][0]) / 2, (celda[0][1] + celda[1][1]) / 2]
        dist = np.linalg.norm(np.array(centro_celda) - np.array(objectiu))
        if dist < min_dist:
            min_dist = dist
            celda_optima = centro_celda

    # Si no hay celdas óptimas, devuelve un vector de velocidad cero
    if celda_optima is None:
        return individuo.get_velocitat_optima()
    
    # Calcula el vector de la posición actual a la celda óptima
    vec = np.array(celda_optima) - np.array(pos)

    # Limita las componentes de la velocidad a v_max
    vec = np.array([min(v_max, abs(component)) * np.sign(component) for component in vec])
    
    return vec.tolist()



def actualitzar_posicio(ind, passadis, dt=1):
    # Obtenir la velocitat actual de l'individu
    velocitat = ind.get_velocitat_optima()

    # Obtenir la posició actual de l'individu
    posicio = ind.get_posicio()

    # Calcular la nova posició
    nova_posicio = np.array(posicio) + np.array(velocitat) * dt

    # Actualitzar la posició de l'individu
    ind.set_posicio(nova_posicio)

    # Obtenim variables rellevants
    objectiu = ind.get_objectiu()
    ind.set_objectiu((nova_posicio[0], objectiu[1]))
    parets = passadis.get_parets()
    radi = ind.get_radi()

    # Verificar si l'individu ha arribat al seu objectiu
    delta = int(passadis.get_n()/20)
    if int(objectiu[1]) == delta and nova_posicio[1] <= objectiu[1]:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
    
    elif objectiu[1] == passadis.get_n() - delta and nova_posicio[1] >= objectiu[1]:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
    
    elif np.linalg.norm(np.array(objectiu) - np.array(nova_posicio)) <= radi:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
    else:
        # # Recalcular la velocitat per orientar-la cap a l'objectiu
        # vector_objectiu = ((objectiu[0] - nova_posicio[0]), (objectiu[1] - nova_posicio[1]))
        # distancia_objectiu = np.linalg.norm(vector_objectiu)
        # ind.set_velocitat_preferida((vector_objectiu / distancia_objectiu) * min(distancia_objectiu, ind.get_v_max()))

        # Correcció de posició per evitar les parets
        min_x, max_x, min_y, max_y = parets
        posicio_corregida = (max(min_x + radi, min(nova_posicio[0], max_x - radi)), max(min_y + radi, min(nova_posicio[1], max_y)))
        ind.set_posicio(tuple(round(num, 2) for num in posicio_corregida))



# # Comprovar, per cada individu, si els punts que hi han entre els segments del rectangle_b interseccionen amb els punts de dins del cercle_a
# # En cas de existir intersecció, afegim a la llista d'interseccions un conjunt amb els punts que intersecten entre rectangle_b i cercle_a
# def calcular_interseccions(individus):
#     interseccions = {}
#     for i in range(len(individus)):
#         ind_a = individus[i]
#         interseccions[ind_a] = []
#         pos_a = np.array(ind_a.get_posicio())
#         radi_moviment = ind_a.get_radi_moviment()
#         print(f"Individu {ind_a.get_id()} té interseccions amb els rectangles de:")

#         for j in range(len(individus)):
#             if individus[j] == ind_a: continue
#             ind_b = individus[j]
#             rectangle_b = ind_b.get_direccio_moviment()
            
#             for segment in rectangle_b:
#                 if intersercta_segment_cercle(segment, pos_a, radi_moviment) == True:
#                     interseccions[ind_a].append(rectangle_b)
#                     print(f"{ind_b.get_id()}")
#                     break

#         print("\n\n")
#     return interseccions

# # Aquesta funció torna True si algun punt del segment intersecta amb el radi i False si no ho fa
# def intersercta_segment_cercle(segment, centre, radi):
#     # Convertim els punts a arrays de Numpy per facilitar els càlculs
#     p_inicial = np.array(segment[0])
#     p_final = np.array(segment[1])
#     centre = np.array(centre)

#     # Calculem el vector del segment i del centre del cercle al punt d'inici
#     v_segment = p_final - p_inicial
#     v_centre_a_inici = p_inicial - centre

#     # Calculem la projecció del vector del centre del cercle al punt d'inici sobre el segment
#     t = - np.dot(v_centre_a_inici, v_segment) / np.dot(v_segment, v_segment)
#     t = np.clip(t, 0, 1) # Ens asegurem que t està entre 0 i 1

#     # Calculem el punt més proper en el segment al centre del cercle
#     p_proper = p_inicial + t * v_segment

#     # Calculem el vector del centre del cercle al punt més proper
#     v_centre_a_proper = p_proper - centre

#     # Si la longitud d'aquest vector és menor o igual al radi del cercle, aleshores hi ha intersecció
#     return np.dot(v_centre_a_proper, v_centre_a_proper) <= radi ** 2


# # Si el punt està dins de la circumferència retorna True, sino retorna False
# def punt_en_circumferencia(punt, centre, radi):
#     x, y = punt
#     xc, yc = centre
#     return (x - xc)**2 + (y - yc)**2 <= radi**2


# # Funció per calcular el temps fins a la col·lisió
# def temps_fins_colisio(ind_a, ind_b):
#     p_rel = ((ind_b.get_posicio()[0] - ind_a.get_posicio()[0], ind_b.get_posicio()[1] - ind_a.get_posicio()[1]))
#     v_rel = ((ind_b.get_velocitat_optima()[0] - ind_a.get_velocitat_optima()[0], ind_b.get_velocitat_optima()[1] - ind_a.get_velocitat_optima()[1]))
#     radi = ind_a.get_radi() + ind_b.get_radi()
#     c = np.dot(p_rel, p_rel) - radi**2

#     # Si els individus ja han col·lidit retorna 0
#     if c < 0:
#         return 0

#     b = np.dot(p_rel, v_rel)
#     # Si els individus s'estan allunyant l'un de l'altre, retorna infinit
#     if b > 0:
#         return float('inf')

#     a = np.dot(v_rel, v_rel)
#     discr = b**2 - a*c

#     # Si no hi ha arrel real, retorna infinit
#     if discr <= 0:
#         return float('inf')

#     # Altrament retorna el temps fins a la col·lisió
#     tau = c / (-b + np.sqrt(discr))
#     return tau

# def actualitzar_posicio(ind, passadis, dt=1):
#     # Obtenir la velocitat actual de l'individu
#     velocitat = ind.get_velocitat_optima()

#     # Obtenir la posició actual de l'individu
#     posicio = ind.get_posicio()

#     # Calcular la nova posició
#     nova_posicio = np.array(posicio) + np.array(velocitat) * dt

#     # Actualitzar la posició de l'individu
#     ind.set_posicio(nova_posicio)

#     # Obtenim variables rellevants
#     objectiu = ind.get_objectiu()
#     ind.set_objectiu((nova_posicio[0], objectiu[1]))
#     parets = passadis.get_parets()
#     radi = ind.get_radi()

#     # Verificar si l'individu ha arribat al seu objectiu
#     delta = int(passadis.get_n()/20)
#     if int(objectiu[1]) == delta and nova_posicio[1] <= objectiu[1]:
#         ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
#         ind.set_posicio(None)
#         passadis.ind_in_passadis.remove(ind)
    
#     elif objectiu[1] == passadis.get_n() - delta and nova_posicio[1] >= objectiu[1]:
#         ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
#         ind.set_posicio(None)
#         passadis.ind_in_passadis.remove(ind)
    
#     elif np.linalg.norm(np.array(objectiu) - np.array(nova_posicio)) <= radi:
#         ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
#         ind.set_posicio(None)
#         passadis.ind_in_passadis.remove(ind)
#     else:
#         # Recalcular la velocitat per orientar-la cap a l'objectiu
#         vector_objectiu = ((objectiu[0] - nova_posicio[0]), (objectiu[1] - nova_posicio[1]))
#         distancia_objectiu = np.linalg.norm(vector_objectiu)
#         ind.set_velocitat_preferida((vector_objectiu / distancia_objectiu) * min(distancia_objectiu, ind.get_v_max()))

#         # Correcció de posició per evitar les parets
#         min_x, max_x, min_y, max_y = parets
#         posicio_corregida = (max(min_x + radi, min(nova_posicio[0], max_x - radi)), max(min_y + radi, min(nova_posicio[1], max_y)))
#         ind.set_posicio(tuple(round(num, 2) for num in posicio_corregida))
