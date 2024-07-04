import classe_trajecte as ct

# Classe Individu en el model Discret
class Individu:
    # Inicialització de la classe Individu
    def __init__(self, id, posicio, sortida, objectiu, velocitat, m, n, camp_visio, ponderacions):
        # Identificador únic per individu
        self.id = id

        # Dupla (x, y) que dona la posicio inicial (entrada) en el passadís
        self.posicio = posicio

        # Llista de duples (x,y) amb les possibles posicions on pot estar l'objectiu       
        self.sortida = sortida

        # Dupla(x, y) posició de l'objectiu de l'individu
        self.objectiu  = objectiu

        # Files passadís
        self.m = m                      
        
        # Carrils passadís
        self.n = n                      
        
        # Velocitat
        self.velocitat = velocitat

        # Direcció respecte l'últim moviment realitzat
        self.direccio = (0,0)

        # Nombre que al elevar el quadrat et dona les cel·les que podrà observar l'individu
        self.camp_visio = camp_visio
        
        # Conté recorregut, temps recorregut, nombre de col·lisions, temps agrupat i els coeficients d'importància
        self.trajecte = ct.Trajecte([posicio], 0, 0, 0, ponderacions) 
        
        # Puntuació utilitzada en l'algorisme genètic per avaluar el rendiment de l'individu al passadís
        self.aptitud = 0       

    # Retorna l'identificador de l'individu
    def get_id(self):
        return self.id

    # Retorna la posició de l'individu
    def get_posicio(self):
        return self.posicio
    
    # Retorna la sortida de l'individu
    def get_sortida(self):
        return self.sortida
    
    # Retorna l'objectiu de l'individu
    def get_objectiu(self):
        return self.objectiu
    
    # Retorna la velocitat de l'individu
    def get_velocitat(self):
         return self.velocitat

    # Retorna la direcció de l'individu
    def get_direccio(self):
        return self.direccio

    # Retorna el trajecte de l'individu
    def get_trajecte(self):
        return self.trajecte
    
    # Retorna el camp de visió de l'individu
    def get_camp_visio(self):
        return self.camp_visio
    
    # Retorna l'aptitud de l'individu
    def get_aptitud(self):
        return self.aptitud
    
    def set_id(self, nou_id):
        self.id = nou_id

    # Estableix una nova posició per a l'individu i l'afegeix al seu recorregut
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.trajecte.recorregut.append(nova_posicio)

    # Estableix un nou objectiu per a l'individu
    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu

    # Estableix una nova direcció per a l'individu
    def set_direccio(self, nova_direccio):
        self.direccio = nova_direccio
    
    # Estableix una nova aptitud per a l'individu
    def set_aptitud(self, nova_aptitud):
        self.aptitud = nova_aptitud