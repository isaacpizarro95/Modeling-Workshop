import random
import utils_passadis as up

# En aquest fitxer configurem els diferents passadissos
# Per simplificar la majoria de variables (potser totes) no podran ser modificades un cop creat el passadis
class Passadis:
    def __init__(self, id, m, n, entrada_unica=False, entrades_laterals=False, obstacles=False):
        self.id = id                                        # identificador únic del passadís per diferenciar-lo
        self.m = m                                          # m files
        self.n = n                                          # n carrils (columnes)
        self.num_entrades = random.randint(n//2, 2*n)       # la quantitat d'entrades es calcula de forma aleatoria i pot agafar valors en el interval [2, n)
        self.entrada_unica = entrada_unica                  # True si tot es entrada o False si hi han entrades concretes
        self.entrades_laterals = entrades_laterals
        self.obstacles = obstacles                          # True si posem obstacles i False si no. Podem afegir un altra variable per descriure els obstacles
        self.ind_in_passadis = []

        # Creació del passadís
        self.elements = up.crear_passadis(m, n, self.num_entrades, entrada_unica, entrades_laterals)
        self.passadis = self.elements[0]
        self.entrades = self.elements[1]
        self.parets = self.elements[2]

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades
        
    def get_num_entrades(self):
        return self.num_entrades

    def get_entrada_unica(self):
        return self.entrada_unica
    
    def get_entrades_laterals(self):
        return self.entrades_laterals

    def get_parets(self):
        return self.parets

    def get_passadis(self):
        return self.passadis
    
    def get_ind_in_passadis(self):
        return self.ind_in_passadis