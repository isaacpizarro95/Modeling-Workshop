import numpy as np

def calcul_nova_velocitat(ind, total_individus):
    pos = np.array(ind.get_posicio())
    objectiu = np.array(ind.get_objectiu())
    grup = ind.get_grup()
    vel = np.array(ind.get_velocitat())
    radi = ind.get_radi()
    v_min = ind.get_v_min()
    v_max = ind.get_v_max()

    inds_agrupats = []
    inds_colisions= []
    dists_agrupats = []
    dists_colisions = []

    for individu in total_individus:
        if individu == ind: continue
        v_rel = vel - np.array(individu.get_velocitat())
        p_rel = pos - np.array(individu.get_posicio())
        dist = np.linalg.norm(p_rel)

        if dist < 2*radi:
            ind.add_colisio()
        #     ind.set_posicio((ind.get_posicio()[0] + 0.15, ind.get_posicio()[1]))
        #     individu.set_posicio((individu.get_posicio()[0] - 0.15, individu.get_posicio()[1]))

        #     v_rel = vel - np.array(individu.get_velocitat())
        #     p_rel = np.array(ind.get_posicio()) - np.array(individu.get_posicio())
        #     dist = np.linalg.norm(p_rel)

        if np.linalg.norm(v_rel) != 0: 
            t_col = (dist - radi - individu.get_radi()) / np.linalg.norm(v_rel)
        else: t_col = (dist - radi - individu.get_radi()) / 0.001

        if t_col >= ind.get_temps_horitzo(): 
            continue
        
        if grup == individu.get_grup():
            pos_ajustada = np.array(individu.get_posicio()) + (2 * radi * np.sign(p_rel))
            inds_agrupats.append(pos_ajustada)
            dists_agrupats.append(dist)
        else:
            pos_ajustada = np.array(individu.get_posicio()) - (2 * radi * np.sign(p_rel))
            inds_colisions.append(pos_ajustada)
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
        nova_direccio = 0.05 * (objectiu - pos) + 0.5 * (mitja_agrupats - pos) - 0.4 * (mitja_colisions - pos)

    # Càlcul nova direcció i nova velocitat
    nova_direccio_norm = nova_direccio / np.linalg.norm(nova_direccio)

    # REVISAR AQUESTES DUES LINIES
    nova_velocitat = v_max * nova_direccio_norm
    nova_velocitat = limits_velocitat(nova_velocitat, v_min, v_max, nova_direccio_norm) 

    ind.set_velocitat(nova_velocitat)

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