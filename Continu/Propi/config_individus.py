# En aquest fitxer configurem els diferents individus
# Les variables: id, camp_visio i objectiu no podran ser modificades
# Posició i velocitat si que podran ser modificades per permetre el moviment i els avançaments.

# Classe Individu en el model Continu
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
        self.velocitat = velocitat              # velocitat actual individu
        self.v_min = v_min
        self.v_max = v_max
        
        # Paràmentres control entorn
        self.radi = radi                      # radi de visió de l'individu
        self.temps_horitzo = temps_horitzo      # temps futur al que mira l'individu per predir el comportament de l'entorn
        self.radi_moviment = v_max + radi
        self.colisions = 0

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
    
    def get_velocitat(self):
         return self.velocitat
    
    def get_colisions(self):
        return self.colisions


    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)
    
    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu

    def set_radi(self, nou_radi):
        self.radi = nou_radi

    def set_velocitat(self, nova_velocitat):
        self.velocitat = nova_velocitat
    
    def add_colisio(self):
        self.colisions += 1