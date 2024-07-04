# Classe Trajecte (forma part de la classe Individu) en el model Discret
class Trajecte:
    def __init__(self, recorregut, n_colisions, t_recorregut, n_agrupat, ponderacions):
        self.recorregut = recorregut  # Recorregut realitzat fins al moment per l'individu (una llista ordenada de les posicions de l'individu)
        self.n_colisions = n_colisions  # Quantitat de col·lisions que ha tingut amb altres individus al llarg del recorregut
        self.t_recorregut = t_recorregut  # Temps (segons) que ha trigat en fer el seu recorregut (equivalent a la quantitat de moviments)
        self.n_agrupat = n_agrupat  # Quantitat de moviments que l'individu ha realitzat agrupat amb altres individus amb una direcció similar al llarg del recorregut
        self.canvis_direccio = 0  # Quantitat de canvis de direcció realitzats durant el recorregut
        self.pes_agrupat = ponderacions[0]  # Coeficient d'importància per a l'agrupament amb altres individus
        self.pes_colisions = ponderacions[1]  # Coeficient d'importància per a les col·lisions
        self.pes_distancia = ponderacions[2]  # Coeficient d'importància per a la distància recorreguda
        self.pes_canvis = ponderacions[3]  # Coeficient d'importància per als canvis de direcció


    # Retorna el recorregut realitzat fins al moment per l'individu (una llista ordenada de les posicions de l'individu)
    def get_recorregut(self):
        return self.recorregut
    
    # Retorna la quantitat de col·lisions que ha tingut amb altres individus al llarg del recorregut
    def get_n_colisions(self):
        return self.n_colisions
    
    # Suma 1 nova col·lisió al sumatori de col·lisions
    def add_colisio(self): 
        self.n_colisions += 1

    # Retorna quants segons (equival a quants moviments) ha trigat en fer el seu recorregut
    def get_t_recorregut(self):
        return self.t_recorregut
    
    # Suma 1 al temps trigat en fer el recorregut
    def add_t_recorregut(self): 
        self.t_recorregut += 1

    # Retorna la quantitat de moviments que ha realitzat agrupat de altres individus amb una direcció similar al llarg del recorregut
    def get_n_agrupat(self):
        return self.n_agrupat

    # Suma 1 als moviments que l'individu ha fet agrupat amb altres individus durant el recorregut
    def add_agrupat(self): 
        self.n_agrupat += 1

    def get_canvis_direccio(self):
        return self.canvis_direccio
    
    # Suma les distancies en cada canvi de direcció realitzat durant el recorregut
    def add_canvi_direccio(self, nova_distancia): 
        self.canvis_direccio += nova_distancia

    # Retorna els coeficients d'importància
    def get_ponderacions(self):
        return [self.pes_agrupat, self.pes_colisions, self.pes_distancia, self.pes_canvis]