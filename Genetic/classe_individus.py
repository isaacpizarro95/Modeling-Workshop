# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

import classe_trajecte as ct

class Individu:
    def __init__(self, id, posicio, sortida, objectiu, velocitat, m, n, camp_visio, ponderacions):
        self.id = id                    # identificador únic per individu
        self.posicio = posicio          # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.sortida = sortida
        self.objectiu  = objectiu       # dupla(x, y) posició de l'objectiu de l'individu
        self.m = m                      # files passadís
        self.n = n                      # carrils passadís
        self.velocitat_maxima = velocitat
        self.direccio = (0,0)
        self.camp_visio = camp_visio
        self.trajecte = ct.Trajecte([posicio], 0, 0, 0, ponderacions) # conté recorregut, temps recorregut, nombre de col·lisions i temps agrupat        

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def get_sortida(self):
        return self.sortida
    
    def get_objectiu(self):
        return self.objectiu
    
    def get_velocitat(self):
         return self.velocitat_maxima

    def get_direccio(self):
        return self.direccio

    def get_trajecte(self):
        return self.trajecte
    
    def get_camp_visio(self):
        return self.camp_visio
    
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.trajecte.recorregut.append(nova_posicio)

    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu

    def set_velocitat(self, nova_velocitat):
        self.velocitat_maxima = nova_velocitat

    def set_direccio(self, nova_direccio):
        self.direccio = nova_direccio