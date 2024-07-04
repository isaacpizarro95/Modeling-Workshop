import random
import utils_passadis as up

# En aquest fitxer configurem els diferents passadissos
# Classe Passadís en el model Continu
class Passadis:
    def __init__(self, id, m, n):
        # Identificador únic del passadís per diferenciar-lo
        self.id = id
        
        # Nombre de files
        self.m = m

        # Nombre de carrils (columnes)
        self.n= n

        # Llista dels individus que es troben al passadís
        self.ind_in_passadis = []

        # Diccionari que conté la posició de cada individu
        self.ind_posicions = {}

        # Obtenció dels segments de rectes que representen les entrades i parets
        self.entrades, self.parets = up.crear_passadis(m, n)

    # Retorna l'identificador del passadís
    def get_id(self):
        return self.id

    # Retorna el nombre de files
    def get_m(self):
        return self.m

    # Retorna el nombre de carrils
    def get_n(self):
        return self.n
    
    # Retorna les entrades
    def get_entrades(self):
        return self.entrades

    # Retorna les parets
    def get_parets(self):
        return self.parets
    
    # Retorna els individus que es troben al passadís
    def get_ind_in_passadis(self):
        return self.ind_in_passadis

    # Retorna el diccionari de posicions
    def get_ind_posicions(self):
        return self.ind_posicions
    
    # def get_obstacles(self):
    #     return self.obstacles