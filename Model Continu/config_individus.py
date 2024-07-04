# Classe Individu en el model Continu
class Individu:
    def __init__(self, id, posicio, sortida, objectiu, grup, v_min, v_max, velocitat, m, n, radi, temps_horitzo):
        # Identificador únic per individu
        self.id = id                           

        # Paràmentres posicionals
        # Dupla (x, y) de la posicio actual de l'individu
        self.posicio = posicio

        # dupla (x, y) de la posicio inicial de l'individu     
        self.entrada = posicio

        # Llista de duples (x,y) amb les possibles posicions on pot estar l'objectiu
        self.sortida = sortida

        # Dupla(x, y) posició de l'objectiu de l'individu
        self.objectiu  = objectiu

        # Classificació segons la sortida de l'individu (pot valdre 0 o 1)
        self.grup = grup

        # Recorregut realitzat fins al moment per l'individu (una llista ordenada de les posicions de l'individu)
        self.recorregut = [posicio]             

        # Files passadís
        self.m = m                              

        # Carrils passadís
        self.n = n                              
        
        # Paràmentres velocitat
        # Velocitat actual individu
        self.velocitat = velocitat    

        # Nombres reals que determinen la velocitat mínima i màxima        
        self.v_min = v_min
        self.v_max = v_max
        
        # Paràmentres control entorn
        # Radi de col·lisió de l'individu
        self.radi = radi                      

        # Temps futur al que mira l'individu per predir el comportament de l'entorn
        self.temps_horitzo = temps_horitzo      
        
        # Radi que determina l'àrea on es poden produir els possibles moviments de l'individu
        self.radi_moviment = v_max + radi

        # Nombre de col·lisions que es tenen al llarg del recorregut
        self.colisions = 0

    # Retorna l'identificador de l'individu
    def get_id(self):
        return self.id

    # Retorna el valor de m
    def get_m(self):
        return self.m
    
    # Retorna el valor de n
    def get_n(self):
        return self.n

    # Retorna la posició actual
    def get_posicio(self):
        return self.posicio
    
    # Retorna la posició per la que el individu ha entrat al passadís
    def get_entrada(self):
        return self.entrada
    
    # Retorna una llista que conté un conjunt de posicions entre les que estan els possibles objectius
    def get_sortida(self):
        return self.sortida
    
    # Retorna la posició de l'objectiu de l'individu
    def get_objectiu(self):
        return self.objectiu
    
    # Retorna el grup al que pertany l'individu (la classificació es fa segons la component y de l'objectiu)
    def get_grup(self):
        return self.grup

    # Retorna el recorregut realitzat fins al moment per l'individu (una llista ordenada de les posicions de l'individu)
    def get_recorregut(self):
        return self.recorregut

    # Retorna el radi de col·lisió de l'individu
    def get_radi(self):
        return self.radi
    
    # Retorna el radi de moviment de l'individu
    def get_radi_moviment(self):
        return self.radi_moviment

    # Retorna el temps d'horitzó de l'individu
    def get_temps_horitzo(self):
        return self.temps_horitzo

    # Retorna el valor mínim que pot prendre la velocitat
    def get_v_min(self):
        return self.v_min
    
    # Retorna el valor màxim que pot prendre la velocitat
    def get_v_max(self):
        return self.v_max
    
    # Retorna la dupla (x,y) amb la velocitat actual
    def get_velocitat(self):
         return self.velocitat
    
    # Retorna la quantitat de col·lisions que s'han donat fins a aquest moment
    def get_colisions(self):
        return self.colisions

    # Estableix una nova posició per a l'individu i l'afegeix al seu recorregut
    def set_posicio(self, nova_posicio):
        self.posicio = nova_posicio
        self.recorregut.append(nova_posicio)
    
    # Estableix un nou objectiu per a l'individu
    def set_objectiu(self, nou_objectiu):
        self.objectiu = nou_objectiu

    # Estableix una nova velocitat per a l'individu
    def set_velocitat(self, nova_velocitat):
        self.velocitat = nova_velocitat
    
    # Afegeix una nova col·lisió al recompte total de col·lisions
    def add_colisio(self):
        self.colisions += 1