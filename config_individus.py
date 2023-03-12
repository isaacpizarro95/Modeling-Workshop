# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

class Individu:
    def __init__(self, id, posicio, m, n):
        self.id = id                    # identificador únic per individu
        self.posicio = posicio        # dupla (x, y) que dona la posicio en el passadis
        self.m = m
        self.n = n
        #self.velocitat = velocitat     # pot prendre valors: 0.25, 0.5, 0.75, 1
        #self.camp_visio = camp_visio   # dupla de enters (i, j) que indica la distància (en quadrats) màxima a la que pot veure l'individu dins del mapa. i mira la fila, j la columna. El camp de visió no es pot modificar un cop establert
        #self.objetiu = objetiu       # dupla (x, y) amb la posició a la que vol arribar l'individu       
        self.recorregut = [posicio]

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)
    
    # def get_velocitat(self):
    #     return self.velocitat

    # def set_velocitat(self, nova_velocitat):
    #     self.velocitat = nova_velocitat

    # def avançar(self):
    #   Fer l'acció de avançar i potser permetre canvi de velocitat
    #   set_posicio(...)

    def moure(self, direccio):
        x, y = self.posicio
        if x == 0 and direccio == 'puja':
            self.set_posicio(None)  # ha arribat al final
        elif x == self.m-1 and direccio == 'baixa':
            self.set_posicio(None)  # ha arribat al final
        elif direccio == 'puja':
            self.set_posicio((x-1, y))
        elif direccio == 'baixa':
            self.set_posicio((x+1, y))

    def get_recorregut(self): # Aquesta funció guardarà el recorregut fet per l'usuari pel passadís
        return self.recorregut