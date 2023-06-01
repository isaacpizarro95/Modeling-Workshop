import pygame
import sys
from pygame.locals import QUIT
import math
import random
import numpy as np

class Individu:
    def __init__(self, id, posicio, sortida, objectiu, grup, v_min, v_max, velocitat, m, n, radi, temps_horitzo):
        self.id = id                            # identificador únic per individu
        # Paràmentres posicionals
        self.posicio = posicio                  # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.entrada = posicio
        self.sortida = sortida
        self.objectiu  = objectiu               # dupla(x, y) posició de la sortida/objectiu de l'individu
        self.grup = grup
        self.recorregut = [posicio]             # llista(vector) que guarda les posicions en les que ha estat l'individu
        self.m = m                              # files passadís
        self.n = n                              # carrils passadís
        
        # Paràmentres velocitat
        self.velocitat_optima = velocitat              # velocitat actual individu
        self.v_min = v_min
        self.v_max = v_max
        self.velocitat_preferida = velocitat    # velocitat estàtica i estandard de l'individu
        
        # Paràmentres control entorn
        self.radi = radi                      # radi de visió de l'individu
        self.temps_horitzo = temps_horitzo      # temps futur al que mira l'individu per predir el comportament de l'entorn
        self.radi_moviment = v_max + radi
        # self.cercle_moviment = None
        # self.direccio_moviment = None

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m
    
    def get_n(self):
        return self.n

    def get_posicio(self):
        return self.posicio
    
    def get_entrada(self):
        return self.entrada
    
    def get_sortida(self):
        return self.sortida
    
    def get_objectiu(self):
        return self.objectiu
    
    def get_grup(self):
        return self.grup

    def get_recorregut(self):
        return self.recorregut

    def get_radi(self):
        return self.radi
    
    def get_radi_moviment(self):
        return self.radi_moviment

    def get_temps_horitzo(self):
        return self.temps_horitzo

    def get_v_min(self):
        return self.v_min
    
    def get_v_max(self):
        return self.v_max
    
    def get_velocitat_optima(self):
         return self.velocitat_optima

    def get_velocitat_preferida(self):
        return self.velocitat_preferida
    
    # def get_cercle_moviment(self):
    #     return self.cercle_moviment
    
    # def get_direccio_moviment(self):
    #     return self.direccio_moviment


    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)
    
    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu

    def set_radi(self, nou_radi):
        self.radi = nou_radi

    def set_velocitat_optima(self, nova_velocitat):
        self.velocitat_optima = nova_velocitat
    
    def set_velocitat_preferida(self, nova_velocitat_preferida):
        self.velocitat_preferida = nova_velocitat_preferida

    # def set_cercle_moviment(self, cercle_moviment):
    #     self.cercle_moviment = cercle_moviment

    # def set_direccio_moviment(self, direccio_moviment):
    #     self.direccio_moviment = direccio_moviment

class Passadis:
    def __init__(self, id, m, n):
        self.id = id
        self.m = m
        self.n= n
        self.ind_in_passadis = []
        self.ind_posicions = {}

        self.entrades, self.parets = crear_passadis(m, n)

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades

    def get_parets(self):
        return self.parets
    
    def get_ind_in_passadis(self):
        return self.ind_in_passadis

    def get_ind_posicions(self):
        return self.ind_posicions
    
    # def get_obstacles(self):
    #     return self.obstacles


def calcul_posicions_entrada(m, n, radi, delta):
    # Crear una lista de todas las posiciones posibles dentro de las entradas
    posiciones = []
    for x in np.arange(radi, m, 2*radi):
        posiciones.append((x, delta))
        posiciones.append((x, n - delta))
    
    # Torna una llista amb tots els segments y las posiciones
    return posiciones


# Calcula la sortida/objectiu a la que anirà l'individu en base a les entrades/sortides disponibles i la seva posició inicial
def calcul_sortida(ind_entrada, entrades):
    for entrada in entrades:
        if esta_dins_segment(ind_entrada, entrada): continue
        else: return entrada


# Genera una posición aleatoria en la salida seleccionada
def calcul_objectiu(sortida):
    x = round(np.random.uniform(sortida[0][0], sortida[1][0]),2)
    y = round(np.random.uniform(sortida[0][1], sortida[1][1]),2)

    return (x, y)


# Calcula la velocitat preferida d'un individu
def calcul_velocidad_preferida(v_min, v_max):
    # Genera una magnitud de velocitat aleatoria en el rang [v_min, v_max]
    magnitud = np.random.uniform(v_min, v_max)

    # Genera una direcció de velocitat aleatoria en el rang [0, 2π]
    direccio = np.random.uniform(0, 2 * np.pi)

    # Calcula las componentes x e y de la velocidad
    vx = magnitud * np.cos(direccio)
    vy = magnitud * np.sin(direccio)

    return np.array((vx, vy))


def crear_passadis(m, n):#, amplada_entrada, entrada_unica, entrades_laterals, obstacles):
    # Creem parets, entrades i obstacles
    parets = crear_parets(m, n)
    delta = n/20 # Distància de les entrades respecte la paret en el eix de la y
    entrades = crear_entrades(m, n, delta)
    #obs = crear_obstacles()

    return entrades, parets#, obs

def crear_parets(m, n):
    min_x = 0
    max_x = m
    min_y = 0
    max_y = n

    # Torna una llista amb tots els segments
    return [min_x, max_x, min_y, max_y]

def crear_entrades(m, n, delta):
    # Crear els segments d'entrada i sortida
    entrada1 = [(0, delta), (m, delta)]
    entrada2 = [(0, n - delta), (m, n - delta)]
    
    # Torna una llista amb tots els segments
    return [entrada1, entrada2]

def esta_dins_segment(punt, segment):
    # Calcula la distancia entre el punt i els dos extrems del segment
    dist_a = np.linalg.norm(np.array(punt) - np.array(segment[0]))
    dist_b = np.linalg.norm(np.array(punt) - np.array(segment[1]))

    # Calcula la llargada del segmento
    llargada_segment = np.linalg.norm(np.array(segment[0]) - np.array(segment[1]))

    # Comprova si la suma de les dos distancies és igual a la llargada del segment (amb un cert marge d'error per tindre en compte la precisió de punt flotant)
    if np.isclose(dist_a + dist_b, llargada_segment, rtol=1e-05):
        return True
    else:
        return False
    

def calcul_nova_velocitat(ind, total_individus):
    pos = np.array(ind.get_posicio())
    objectiu = np.array(ind.get_objectiu())
    grup = ind.get_grup()
    vel = np.array(ind.get_velocitat_optima())
    radi = ind.get_radi()
    v_min = ind.get_v_min()
    v_max = ind.get_v_max()

    inds_agrupats = []
    inds_colisions= []
    dists_agrupats = []
    dists_colisions = []

    for individu in total_individus:
        if individu == ind: continue
        v_rel = vel - np.array(individu.get_velocitat_optima())
        p_rel = pos - np.array(individu.get_posicio())
        dist = np.linalg.norm(p_rel)

        if dist < radi*2:
            ind.set_posicio((ind.get_posicio()[0] + 0.15, ind.get_posicio()[1]))
            individu.set_posicio((individu.get_posicio()[0] - 0.15, individu.get_posicio()[1]))

            v_rel = vel - np.array(individu.get_velocitat_optima())
            p_rel = np.array(ind.get_posicio()) - np.array(individu.get_posicio())
            dist = np.linalg.norm(p_rel)

        if np.linalg.norm(v_rel) != 0: 
            t_col = (dist - radi - individu.get_radi()) / np.linalg.norm(v_rel)
        else: t_col = (dist - radi - individu.get_radi()) / 0.001

        if t_col >= ind.get_temps_horitzo(): 
            continue
        
        if grup == individu.get_grup():
            inds_agrupats.append(np.array(individu.get_posicio()))
            dists_agrupats.append(dist)
        else:
            inds_colisions.append(np.array(individu.get_posicio()))
            dists_colisions.append(dist)
        
    if inds_agrupats: 
        pesos_agr = np.reciprocal(dists_agrupats)
        pesos_agr = np.where(pesos_agr == np.inf, 1e10, pesos_agr)
        mitja_agrupats = np.average(np.array(inds_agrupats), axis=0, weights=pesos_agr)
    else:
        mitja_agrupats = pos

    if inds_colisions: 
        pesos_col = np.reciprocal(dists_colisions)
        pesos_col = np.where(pesos_col == np.inf, 1e10, pesos_col)
        mitja_colisions = np.average(np.array(inds_colisions), axis=0, weights=pesos_col)
    else: 
        mitja_colisions = pos

    # Control de decisió del moviment
    if abs(pos[1] - objectiu[1]) <= 0.2 * abs(ind.get_entrada()[1] - objectiu[1]):
        nova_direccio = 0.5 * (objectiu - pos) + 0.2 * (mitja_agrupats - pos) - 0.3 * (mitja_colisions - pos)
    elif len(inds_agrupats) > len(inds_colisions):
        nova_direccio = 0.05 * (objectiu - pos) + 0.9 * (mitja_agrupats - pos) - 0.05 * (mitja_colisions - pos)
    elif len(inds_agrupats) <= len(inds_colisions):
        nova_direccio = 0.05 * (objectiu - pos) + 0.5 * (mitja_agrupats - pos) - 0.45 * (mitja_colisions - pos)

    # Càlcul nova direcció i nova velocitat
    nova_direccio_norm = nova_direccio / np.linalg.norm(nova_direccio)
    nova_velocitat = v_max * nova_direccio_norm
    nova_velocitat = limits_velocitat(nova_velocitat, v_min, v_max, nova_direccio_norm) 

    ind.set_velocitat_optima(nova_velocitat)


def limits_velocitat(vel, v_min, v_max, direccio):
    nova_velocitat = vel
    nova_velocitat_magnitude = np.linalg.norm(vel)
    
    if nova_velocitat_magnitude < v_min:
        nova_velocitat = direccio * v_min
    elif nova_velocitat_magnitude > v_max:
        nova_velocitat = direccio * v_max
    return nova_velocitat


def actualitzar_posicio(ind, passadis):
    # Obtenir la velocitat actual de l'individu
    velocitat = ind.get_velocitat_optima()

    # Obtenir la posició actual i el radi de l'individu
    posicio = ind.get_posicio()
    radi = ind.get_radi()

    # Calcular la nova posició
    nova_posicio = np.array(posicio) + np.array(velocitat)

    # Actualitzar la posició de l'individu
    ind.set_posicio(nova_posicio)
    passadis.ind_posicions[ind] = nova_posicio

    # Obtenim variables rellevants
    objectiu = ind.get_objectiu()
    ind.set_objectiu((nova_posicio[0], objectiu[1]))
    parets = passadis.get_parets()
    radi = ind.get_radi()

    # Verificar si l'individu ha arribat al seu objectiu
    delta = passadis.get_n()/20
    if objectiu[1] == delta and nova_posicio[1] <= objectiu[1]:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
        del passadis.ind_posicions[ind]
    
    elif objectiu[1] == passadis.get_n() - delta and nova_posicio[1] >= objectiu[1]:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
        del passadis.ind_posicions[ind]
    
    elif np.linalg.norm(np.array(objectiu) - np.array(nova_posicio)) <= radi:
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))
        ind.set_posicio(None)
        passadis.ind_in_passadis.remove(ind)
        del passadis.ind_posicions[ind]
    
    else:
        # Correcció de posició per evitar les parets
        min_x, max_x, min_y, max_y = parets
        posicio_corregida = (max(min_x + radi, min(nova_posicio[0], max_x - radi)), max(min_y + radi, min(nova_posicio[1], max_y)))
        ind.set_posicio(tuple(round(num, 2) for num in posicio_corregida))
        passadis.ind_posicions[ind] = ind.get_posicio()


def dibuixar_passadis_pygame(n, m, passadis, individus, scale_x, scale_y, screen, clock, fps):
    # Definim els colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (128, 128, 128)
    color_entrada1 = (0, 0, 255)  # Azul
    color_entrada2 = (255, 0, 0)  # Rojo

    # Asociar las entradas con los colores
    entrades = passadis.get_entrades()
    entrades_colors = {tuple(entrades[0]): color_entrada1, tuple(entrades[1]): color_entrada2}

    # Per parar la simulació quan vulguem
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # "Netejar" pantalla
    screen.fill(white)

    # De igual manera, al dibujar las lineas debes aplicar el factor de escala a las coordenadas
    pygame.draw.line(screen, color_entrada1, tuple(np.array(entrades[0][0]) * [scale_x, scale_y]), tuple(np.array(entrades[0][1]) * [scale_x, scale_y]), 3)
    pygame.draw.line(screen, color_entrada2, tuple(np.array(entrades[1][0]) * [scale_x, scale_y]), tuple(np.array(entrades[1][1]) * [scale_x, scale_y]), 3)
    
    for individu in individus:
        pos = individu.get_posicio()
        
        # El individuo ha salido del mapa
        if pos is None:  continue
        # Obtener el color de la salida de este individuo
        color_individu = entrades_colors[tuple(individu.get_sortida())]
        # Obtener la posición del individuo y aplicar el factor de escala

        pos = (int(pos[0]*scale_x), int(pos[1]*scale_y))
        #print(f"Posición escalada: {pos}")

        radius = individu.get_radi() * min(scale_x, scale_y)
        # Dibujar el individuo con ese color
        pygame.draw.circle(screen, color_individu, pos, 1)  # Dibuja el punto central
        pygame.draw.circle(screen, color_individu, pos, radius, 1)  # Dibuja la circunferencia

        # Dibujar flecha de dirección
        velocitat = individu.get_velocitat_optima()

        if np.linalg.norm(velocitat) != 0:  # Skip if velocity is zero
            # Normalizar la velocidad para obtener la dirección
            direccion = velocitat / np.linalg.norm(velocitat)

            # Escalar la dirección para que la flecha tenga un tamaño constante
            direccion *= 15

            # Calcular los puntos para el triángulo de la flecha
            punta = tuple(pos + direccion)

            draw_arrow(screen, color_individu, pos, punta, 10)  # Dibuja la flecha
    
    pygame.display.flip()
    clock.tick(fps)  # Limitar a 60 FPS


# Dibuixa la fletxa que indica la direcció de cada individu
def draw_arrow(screen, color, start, end, arrow_head_size):
    dx = int(end[0] - start[0])
    dy = int(end[1] - start[1])
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return
    udx = dx / length
    udy = dy / length
    arrow_head_angle = math.pi / 6
    arrow_tail = (end[0] - udx * arrow_head_size, end[1] - udy * arrow_head_size)
    arrow_left = (
        arrow_tail[0] - udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        arrow_tail[1] + udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    arrow_right = (
        arrow_tail[0] + udy * arrow_head_size * math.tan(arrow_head_angle / 2),
        arrow_tail[1] - udx * arrow_head_size * math.tan(arrow_head_angle / 2),
    )
    pygame.draw.line(screen, color, start, arrow_tail, 1)
    pygame.draw.polygon(screen, color, [end, arrow_left, arrow_right])

def simulacio_2D(passadis, num_iteracions, aforament, fps):
    m = passadis.get_m()
    n = passadis.get_n()
    entrades = passadis.get_entrades()  # Obtenim les entrades/sortides del passadís

    # Inicializar Pygame
    pygame.init()

    # Obtener el tamaño de la pantalla del dispositivo
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w * 0.5
    screen_height = screen_info.current_h * 0.9

    # Calcular el factor de escala
    scale_x = screen_width / m
    scale_y = screen_height / n

    # Crear la ventana
    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))

    # Crear un reloj para controlar la velocidad de actualización de la pantalla
    clock = pygame.time.Clock()

    # Parametres dels individus
    id_individu = 0 
    v_min = 0.02
    v_max = 0.2
    radi = 0.3
    temps_horitzo = 3
    delta = n/20

    # Comptem i classifiquem les interaccions entre els individus
    colisions = 0
    interaccions = 0

    # Simulem el moviment dels individus a cada interació
    individus = []
    velocitats = {}

    for t in range(num_iteracions):
        if t % 2 == 0:
            # Creem un nombre aleatori d'individus que anirá de 0 al màxim que ens permeti l'aforament' tenint en compte els individus que ja hi han 
            nous_individus = random.randint(0, (aforament-len(passadis.ind_in_passadis))//10)
            if nous_individus > int(m/(2*radi)) - 1: nous_individus = int(m/(2 * radi)) - 1

            # Dividim les entrades segons el radi dels individus
            posicions_entrades = calcul_posicions_entrada(m, n, radi, delta)

            # Afegim els individus nous que apareixen a les entrades i els afegim a la llista
            for j in range(1, nous_individus + 1):
                # if len(passadis.ind_in_passadis) >= aforament - 2: break
                # for k in range(2):
                # Calculem el id del nou individu
                id_individu += 1

                # Calculem l'entrada de l'individu
                index_entrada = random.randrange(len(posicions_entrades))
                entrada = posicions_entrades[index_entrada]
                posicions_entrades.pop(index_entrada)
                
                # Calculem la sortida i l'objectiu
                sortida = calcul_sortida(entrada, entrades)
                objectiu = calcul_objectiu(sortida)

                # Classifiquem a l'individu segons el seu objectiu
                if objectiu[1] == delta: grup = 0
                else: grup = 1

                # Calculem la velocitat preferida
                velocitat = calcul_velocidad_preferida(v_min, v_max)

                # Creem el nou individu amb els paràmetres i variables calculats previament
                individu = Individu(id_individu, entrada, sortida, objectiu, grup, v_min, v_max, velocitat, m, n, radi, temps_horitzo)
                
                # Afegim a l'individu a la llista total, a l'aforament del passadís
                individus.append(individu)
                passadis.ind_in_passadis.append(individu)
                passadis.ind_posicions[individu] = entrada
                velocitats[individu] = []
        
        for ind in passadis.get_ind_in_passadis():
            calcul_nova_velocitat(ind, passadis.get_ind_in_passadis())
            actualitzar_posicio(ind, passadis)
            velocitats[ind].append(ind.get_velocitat_optima())

        # Mostrem quants individus hi han al passadís en el instant 't' de temps
        print(f"Quantitat d'invididus en t = {t} = {len(passadis.ind_in_passadis)}\n")
        print(f"Total invididus en t = {t} = {len(individus)}\n")

        # Dibuixem el passadís en cada unitat de temps
        dibuixar_passadis_pygame(n, m, passadis, individus, scale_x, scale_y, screen, clock, fps)

        
    #recorreguts = []
    finalitzats = 0
    datos = []
    for ind in individus:
        if ind.get_recorregut()[-1] == None: finalitzats += 1
        print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha tingut velocitat mitja: {np.average(velocitats[ind])}\n")
        #print(f"L'individu {ind.get_id()}, amb objectiu {tuple(round(num, 2) for num in ind.get_objectiu())} ha fet el recorregut:\n{ind.get_recorregut()}\n")
        #recorreguts.append(ind.get_recorregut())
        datos.append(abs(np.average(velocitats[ind])))
    print(f"Han arribat al seu objectiu {finalitzats} individus dels {len(individus)} totals\n")

cas1 = Passadis(0, 15, 20)
simulacio_2D(cas1, 2000, 100, 40)