import numpy as np

# Aquesta funció ens ensenya que la distribució de probabilitats esta feta tal com voliem. Es només una comprovació
def comprovacio_probabilitat_velocitats():
    velocitats = [0.25, 0.5, 0.75, 1]
    probabilitats = [0.15, 0.25, 0.35, 0.25]

    x_values = []
    for i in range(200):
        x = np.random.choice(velocitats, p=probabilitats)
        x_values.append(x)

    counts = [x_values.count(v) for v in velocitats]
    percentages = [count / len(x_values) * 100 for count in counts]

    for v, p in zip(velocitats, percentages):
        print(f'El {p:.2f}% dels valors de x son {v}')

comprovacio_probabilitat_velocitats()


# Explicació funció np.count_nonzero()
"""
La funció np.count_nonzero() de NumPy no itera explícitament per tots els valors de la matriu. En lloc d'això, utilitza la capacitat de 
NumPy per realitzar operacions vectoritzades per comptar els elements de la matriu que compleixen una determinada condició.

Internament, np.count_nonzero() rep com a argument una expressió booleana que avalua si cada element de la matriu compleix una determinada 
condició. Per comptar la quantitat d'elements que compleixen la condició, NumPy utilitza una tècnica coneguda com a "reducció".

La reducció és una tècnica de programació que consisteix a aplicar una operació a tots els elements d'una matriu i reduir el resultat a un
sol valor. En el cas de np.count_nonzero(), l'operació que s'aplica és la comparació d'igualtat entre els elements de la matriu i el valor 
que es vol comptar.

La tècnica de reducció utilitzada per NumPy per comptar els elements d'una matriu es basa en la segmentació de la matriu en blocs més petits. 
En lloc d'iterar per tots els elements de la matriu, NumPy divideix la matriu en blocs i compta els elements que compleixen la condició en 
cada bloc. Després, suma els resultats parcials per obtenir el número total d'elements que compleixen la condició.

Aquest enfocament de segmentació i suma és molt més eficient que iterar explícitament per tots els elements de la matriu, especialment en 
matrius grans. D'aquesta manera, NumPy pot comptar la quantitat d'elements que compleixen una condició de manera eficient i sense recórrer 
explícitament tota la matriu.
"""

# Explicació funció random.choice()
"""
La funció random.choice() serveix per seleccionar un element aleatori d'una seqüència, com ara una llista, una tupla o una cadena de caràcters.
El segón paràmetre asigna una probabilitat de 0 a 1 de triar un dels elements de la seqüència del primer paràmetre.
"""

# Explicació funció random.sample()
"""
La funció random.sample() és una funció que pren dos arguments: una seqüència (com una llista, tupla o conjunt) i un nombre enter k. 
Retorna una llista amb k elements escollits de forma aleatòria de la seqüència.
"""

# Explicació funció np.array.shape[]
"""
Obté el nombre de files o columnes d'una matriu.
np.array.shape[0] indica el nombre de files.
np.array.shape[1] indica el nombre de columnes.
"""

# Explicació funció np.linalg.norm()
"""
L'expressió np.linalg.norm(np.array(objectiu) - np.array(individu.get_posicio())) calcula la norma Euclidiana del vector resultant de la resta entre 
el vector de posició de l'objectiu objectiu i el vector de posició actual de lindividu individu.

En altres paraules, si p1 és el vector de posició dobjectiu i p2 és el vector de posició actual dindividu, llavors el vector resultant de la 
resta p1-p2 és un vector que apunta des de p2 cap a p1. La norma Euclidiana daquest vector representa la distància entre p1 i p2. 
La funció np.linalg.norm calcula precisament això, és a dir, la longitud o la magnitud d'aquest vector, que és la distància entre l'objectiu i 
l'individu en qüestió.
"""