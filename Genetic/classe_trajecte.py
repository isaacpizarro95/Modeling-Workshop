class Trajecte:
    def __init__(self, recorregut, n_colisions, t_recorregut, n_agrupat, ponderacions):
        self.recorregut = recorregut
        self.n_colisions = n_colisions
        self.t_recorregut = t_recorregut
        self.n_agrupat = n_agrupat
        self.canvis_direccio = 0
        self.pes_agrupat = ponderacions[0]
        self.pes_colisions = ponderacions[1]
        self.pes_distancia = ponderacions[2]
        self.pes_canvis = ponderacions[3]

    def get_recorregut(self):
        return self.recorregut
    
    def get_n_colisions(self):
        return self.n_colisions
    
    def add_colisio(self): # Suma 1 nova col·lisió al sumatori de col·lisions
        self.n_colisions += 1

    def get_t_recorregut(self):
        return self.t_recorregut
    
    def add_t_recorregut(self): # Suma 1 al temps trigat en fer el recorregut
        self.t_recorregut += 1
    
    def get_n_agrupat(self):
        return self.n_agrupat

    def add_agrupat(self): # Suma 1 als moviments que l'individu ha fet agrupat amb altres individus durant el recorregut
        self.n_agrupat += 1

    def get_canvis_direccio(self):
        return self.canvis_direccio
    
    def add_canvi_direccio(self): # Suma 1 al sumatori referent a la quantitat de canvis de direcció realitzats durant el recorregut
        self.canvis_direccio += 1

    def get_ponderacions(self):
        return self.pes_agrupat, self.pes_colisions, self.pes_distancia, self.pes_canvis