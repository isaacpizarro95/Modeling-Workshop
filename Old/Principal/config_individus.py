# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

class Individu:
    def __init__(self, id, posicio, sortida, objectiu, direccio, velocitat, m, n):
        self.id = id                    # identificador únic per individu
        self.posicio = posicio          # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.sortida = sortida          # vector [(x_1, y_1),...,(x_n, y_n)] amb les possibles posicions de sortida/objectiu de l'individu
        self.objectiu  = objectiu       # dupla (x, y) que dona la posicio objectiu de l'individu en el passadís
        self.direccio = direccio
        self.recorregut = [posicio]     # llista(vector) que guarda les posicions en les que ha estat l'individu
        self.m = m                      # files passadís
        self.n = n                      # carrils passadís
        self.velocitat = velocitat      # pot prendre valors: 0.25, 0.5, 0.75, 1. AIXO S'HA DE REDEFINIR
        self.radi_visio = 10            # dupla de enters (i, j) que indica la distància (en quadrats) màxima a la que pot veure l'individu dins del mapa. i mira la fila, j la columna. El camp de visió no es pot modificar un cop establert     

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)

    def get_sortida(self):
        return self.sortida
    
    def get_objectiu(self):
        return self.objectiu
    
    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu
    
    def get_direccio(self):
        return self.direccio
    
    def set_direccio(self, nova_direccio):
        self.direccio = nova_direccio
    
    def get_recorregut(self):
        return self.recorregut
    
    def get_velocitat(self):
         return self.velocitat
    
    def set_velocitat(self, nova_velocitat):
        self.velocitat = nova_velocitat
    
    def get_radi_visio(self):
        return self.radi_visio

    def set_radi_visio(self, nou_radi):
        self.radi_visio = nou_radi