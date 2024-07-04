import numpy as np

def calcul_nova_velocitat(ind, total_individus):
    """
    Calcula la nova velocitat per a un individu en funció de la seva posició, objectiu i els individus propers.

    Paràmetres:
    ind (objecte Individu): L'individu per al qual es calcularà la nova velocitat.
    total_individus (llista d'objectes Individu): Tots els individus del passadís.

    Actualitza la velocitat de l'individu indicant la direcció i magnitud en que moure's
    """
    # Posició de l'individu
    pos = np.array(ind.get_posicio())

    # Objectiu de l'individu
    objectiu = np.array(ind.get_objectiu()) 

    # Grup de l'individu
    grup = ind.get_grup() 

    # Velocitat actual de l'individu
    vel = np.array(ind.get_velocitat()) 

    # Radi de l'individu
    radi = ind.get_radi()

    # Velocitat mínima i màxima de l'individu
    v_min = ind.get_v_min() 
    v_max = ind.get_v_max()

    # Llista de posicions per a individus del mateix grup
    inds_agrupats = [] 

    # Llista de posicions per a individus d'un altre grup
    inds_colisions = [] 

    # Llista de distàncies a individus del mateix grup
    dists_agrupats = [] 

    # Llista de distàncies a individus d'un altre grup
    dists_colisions = [] 

    # Calcular les posicions ajustades segons el radi i les distàncies als individus propers
    for individu in total_individus:
        if individu == ind:
            continue

        # Velocitat relativa respecte a un altre individu
        v_rel = vel - np.array(individu.get_velocitat()) 

        # Posició relativa respecte a un altre individu
        p_rel = pos - np.array(individu.get_posicio()) 

        # Distància euclidiana respecte a un altre individu
        dist = np.linalg.norm(p_rel) 

        # Actualitzar el comptador de col·lisions si la distància és menor a dos radis
        if dist < 2*radi: 
            ind.add_colisio() 

        # Calcular el temps estimat de col·lisió amb un altre individu
        if np.linalg.norm(v_rel) != 0:
            t_col = (dist - radi - individu.get_radi()) / np.linalg.norm(v_rel) 
        else:
            t_col = (dist - radi - individu.get_radi()) / 0.001

        # Si el temps de col·lisió és major o igual que el temps d'hortizó de l'individu aleshores no tenim en compte a l'altre individu
        if t_col >= ind.get_temps_horitzo():
            continue
        
        # Ajustem la posició de l'altre individu segons el radi i la direcció de l'altre individu i l'afegim a la llista de posicions agrupades
        # Calculem també la distància fins a aquesta posició i l'afegim a la llista de distàncies
        if grup == individu.get_grup():
            pos_ajustada = np.array(individu.get_posicio()) + (2 * radi * np.sign(p_rel)) 
            inds_agrupats.append(pos_ajustada)
            dists_agrupats.append(dist)

        # Ajustem la posició de l'altre individu segons el radi i la direcció de l'altre individu i l'afegim a la llista de posicions en col·lisió
        # Calculem també la distància fins a aquesta posició i l'afegim a la llista de distàncies
        else:
            pos_ajustada = np.array(individu.get_posicio()) - (2 * radi * np.sign(p_rel)) 
            inds_colisions.append(pos_ajustada)
            dists_colisions.append(dist)
        
    if inds_agrupats:
        # Calculem els inversos de les distàncies als individus agrupats
        pesos_agr = np.reciprocal(dists_agrupats)
        pesos_agr = np.where(pesos_agr == np.inf, 1e10, pesos_agr)

        # Mitjana ponderada utilitzant els inversos de les distàncies i les posicions ajustades dels individus agrupats
        mitja_agrupats = np.average(np.array(inds_agrupats), axis=0, weights=pesos_agr) 
    else:
        mitja_agrupats = pos

    if inds_colisions:
        # Calculem els inversos de les distàncies als individus amb potencial col·lisió
        pesos_col = np.reciprocal(dists_colisions)
        pesos_col = np.where(pesos_col == np.inf, 1e10, pesos_col)
        # Mitjana ponderada utilitzant els inversos de les distàncies i les posicions ajustades dels individus amb potencial col·lisió
        mitja_colisions = np.average(np.array(inds_colisions), axis=0, weights=pesos_col)
    else:
        mitja_colisions = pos

    """
    Tenint en compte la mitjana dels individus agrupats, la mitjana dels individus en direcció contraria i la posició de l'objectiu
    tenim un triangle en el que ens podem moure per tots els punts de l'interior depenent dels valors dels coeficients d'importància
    que multiplicaran amb un valor entre 0 i 1 els tres punts del triangle esmentats.
    """

    # Control de decisió del moviment
    # Si l'individu està aprop de l'objectiu prioritza la posició de l'objectiu en el càlcul de la nova direcció
    if abs(pos[1] - objectiu[1]) <= 0.2 * abs(ind.get_entrada()[1] - objectiu[1]):
        nova_direccio = 0.5 * (objectiu - pos) + 0.2 * (mitja_agrupats - pos) - 0.3 * (mitja_colisions - pos) 

    # Si dins del temps d'horitzó hi han més individus agrupats que potencials col·lisions es prioritza la mitjana dels individus agrupats
    elif len(inds_agrupats) > len(inds_colisions):
        nova_direccio = 0.05 * (objectiu - pos) + 0.9 * (mitja_agrupats - pos) - 0.05 * (mitja_colisions - pos) 
    
    # Si dins del temps d'horitzó hi han més individus col·lisionadors que agrupats s'equilibra la prioritat entre els dos grups d'individus
    elif len(inds_agrupats) <= len(inds_colisions):
        nova_direccio = 0.05 * (objectiu - pos) + 0.5 * (mitja_agrupats - pos) - 0.4 * (mitja_colisions - pos) 

    # Normalitza la nova direcció dividint el vector 'nova_direccio' per la seva norma. 
    # Això garantitza que la magnitud del vector sigui igual a 1 però mantenint la direcció que haviem calculat prèviament
    nova_direccio_norm = nova_direccio / np.linalg.norm(nova_direccio)

    # Fem un primer càlcul de la velocitat a partir del valor màxim que poden tenir les components del vector i de la direcció calculada
    nova_velocitat = v_max * nova_direccio_norm

    # Aquesta funció garanteix que la velocitat estigui dins dels límits establerts per 'v_min' i 'v_max' 
    # També ajusta la velocitat segons la direcció de moviment representada per 'nova_direccio_norm'.
    nova_velocitat = limits_velocitat(nova_velocitat, v_min, v_max, nova_direccio_norm) 

    # Actualització de la nova velocitat de l'individu
    ind.set_velocitat(nova_velocitat) 


def limits_velocitat(vel, v_min, v_max, direccio):
    """
    Limita la velocitat d'un vector a un rang específic ajustant-lo als límits establerts.

    Paràmetres:
    vel (np.array): Vector de velocitat original.
    v_min (float): Valor mínim de velocitat permès.
    v_max (float): Valor màxim de velocitat permès.
    direccio (np.array): Vector de direcció del moviment.

    Retorna:
    np.array: Vector de velocitat modificat, ajustat als límits especificats.
    """

    nova_velocitat = vel

    # Calculem la magnitud de la velocitat
    nova_velocitat_magnitude = np.linalg.norm(vel)
    
    # Comprovem si la magnitud de la velocitat està per sota del valor mínim
    if nova_velocitat_magnitude < v_min:
        # Si és inferior, ajustem la velocitat a la direcció multiplicada pel valor mínim
        nova_velocitat = direccio * v_min
    
    # Comprovem si la magnitud de la velocitat està per sobre del valor màxim
    elif nova_velocitat_magnitude > v_max:
        # Si és superior, ajustem la velocitat a la direcció multiplicada pel valor màxim
        nova_velocitat = direccio * v_max

    return nova_velocitat


def actualitzar_posicio(ind, passadis):
    """
    Actualitza la posició de l'individu en el passadís.

    Paràmetres:
    ind (objecte individu): L'individu a actualitzar la posició.
    passadis: L'objecte passadís que conté la configuració del passadís.

    """
    
    # Obtenir la velocitat actual de l'individu
    velocitat = ind.get_velocitat()

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
    # Calculem la distància delta com una fracció de la dimensió de la matriu
    delta = passadis.get_n() / 20  

    # Verifiquem si l'objectiu de l'individu està a una distància delta a la primera fila i si la nova posició en l'eix y és menor o igual a l'objectiu
    if objectiu[1] == delta and nova_posicio[1] <= objectiu[1]:  
        # Actualitzem la posició de l'individu
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))  

        # Eliminem la posició de l'individu
        ind.set_posicio(None)  

        # Eliminem l'individu de la llista d'individus del passadís
        passadis.ind_in_passadis.remove(ind)  

        # Eliminem l'individu del diccionari de posicions del passadís
        del passadis.ind_posicions[ind]  
    
    # Verifiquem si l'objectiu de l'individu està a una distància delta a l'última fila i si la nova posició en l'eix y és major o igual a l'objectiu
    elif objectiu[1] == passadis.get_n() - delta and nova_posicio[1] >= objectiu[1]:  
        # Actualitzem la posició de l'individu
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))  

        # Eliminem la posició de l'individu
        ind.set_posicio(None)  

        # Eliminem l'individu de la llista d'individus del passadís
        passadis.ind_in_passadis.remove(ind)  

        # Eliminem l'individu del diccionari de posicions del passadís
        del passadis.ind_posicions[ind]  
    
    # Verifiquem si la distància entre l'objectiu i la nova posició és menor o igual al radi de l'individu
    elif np.linalg.norm(np.array(objectiu) - np.array(nova_posicio)) <= radi:  
        # Actualitzem la posició de l'individu
        ind.set_posicio(tuple(round(num, 2) for num in nova_posicio))  

        # Eliminem la posició de l'individu
        ind.set_posicio(None)  

        # Eliminem l'individu de la llista d'individus del passadís
        passadis.ind_in_passadis.remove(ind)  

        # Eliminem l'individu del diccionari de posicions del passadís
        del passadis.ind_posicions[ind]

    # Si cap de les condicions anteriors és verificada
    else:  
        # Obtenim els valors de les coordenades de les parets
        min_x, max_x, min_y, max_y = parets  
        # Corregim la posició per evitar les parets
        posicio_corregida = (max(min_x + radi, min(nova_posicio[0], max_x - radi)), max(min_y + radi, min(nova_posicio[1], max_y)))  
        # Actualitzem la posició de l'individu
        ind.set_posicio(tuple(round(num, 2) for num in posicio_corregida))
        passadis.ind_posicions[ind] = ind.get_posicio()
