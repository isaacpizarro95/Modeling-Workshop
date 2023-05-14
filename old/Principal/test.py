def distancia_euclidiana(a, b):
    return ((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5

sortida = [(0,1), (0,2), (0,3), (0,4)]
entrada = (11,2)

def calcul_objectiu(posicio, sortida):
    if type(sortida) != tuple:
        aux = distancia_euclidiana(posicio, sortida[0])
        objectiu = sortida[0]
        for pos in sortida:
            if distancia_euclidiana(posicio, pos) < aux:
                objectiu = pos
                aux = distancia_euclidiana(posicio, pos)

    else:
        #aux = distancia_euclidiana(posicio, sortida)
        objectiu = sortida

    return objectiu

objectiu = calcul_objectiu(entrada, sortida)
print(f"Objectiu = {objectiu}\n")
print(f"Entrada = {entrada}\n")
print(f"Objectiu = {calcul_objectiu(entrada, objectiu)}\n")