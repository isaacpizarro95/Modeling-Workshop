# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

class Individu:
    def __init__(self, id, posicio, objectiu, velocitat, m, n, radi, temps_horitzo):
        self.id = id                            # identificador únic per individu
        self.posicio = posicio                  # dupla (x, y) que dona la posicio inicial (entrada) en el passadis
        self.objectiu  = objectiu               # dupla(x, y) posició de la sortida/objectiu de l'individu
        self.recorregut = [posicio]             # llista(vector) que guarda les posicions en les que ha estat l'individu
        self.m = m                              # files passadís
        self.n = n                              # carrils passadís
        self.velocitat = velocitat              # velocitat actual individu
        self.velocitat_preferida = velocitat    # velocitat estàtica i estandard de l'individu
        self.radi = radi                        # radi de visió de l'individu
        self.temps_horitzo = temps_horitzo      # temps futur al que mira l'individu per predir el comportament de l'entorn

    def get_id(self):
        return self.id

    def get_posicio(self):
        return self.posicio
    
    def get_objectiu(self):
        return self.objectiu
    
    def get_velocitat(self):
         return self.velocitat

    def get_recorregut(self):
        return self.recorregut

    def get_radi(self):
        return self.radi

    def get_temps_horitzo(self):
        return self.temps_horitzo

    def get_velocitat_preferida(self):
        return self.velocitat_preferida


    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)

    def set_radi(self, nou_radi):
        self.radi = nou_radi

    def set_temps_horitzo(self, nou_temps_horitzo):
        self.temps_horitzo = nou_temps_horitzo

    def set_velocitat_preferida(self, nova_velocitat_preferida):
        self.velocitat_preferida = nova_velocitat_preferida