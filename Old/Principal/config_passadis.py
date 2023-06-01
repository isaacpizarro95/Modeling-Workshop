import random
import utils_passadis as up

# En aquest fitxer configurem els diferents passadissos
# Per simplificar la majoria de variables (potser totes) no podran ser modificades un cop creat el passadis
class Passadis:
    def __init__(self, id, m, n, amplada_entrada = 1, entrada_unica=False, entrades_laterals=False, obstacles=False):
        self.id = id                                        # identificador únic del passadís per diferenciar-lo
        self.m = m                                        # m files (sumem 2 files per les parets)
        self.n = n                                        # n carrils (columnes) (sumem 2 columnes per les parets)
        self.amplada_entrada = amplada_entrada              # enter que determina quantes cel·les ocupa cada entrada
        # la quantitat d'entrades es calcula de forma aleatoria i pot agafar valors en el interval [a, b)
        if entrada_unica == True:
            self.num_entrades = random.randint(n//amplada_entrada, ((2*n)-4)//amplada_entrada)  
        else: self.num_entrades = random.randint(m//amplada_entrada, ((2*(n+m))-4)//amplada_entrada)
        self.entrada_unica = entrada_unica                  # True si tot es entrada o False si hi han entrades concretes
        self.entrades_laterals = entrades_laterals          # True si hi han entrades als laterals o False si no n'hi han
        self.obstacles = obstacles                          # True si posem obstacles i False si no. Podem afegir un altra variable per descriure els obstacles
        self.ind_in_passadis = []                           # Llista dels individus que hi han al passadís a cada instant de temps t

        # Creació del passadís
        self.passadis, self.entrades, self.parets = up.crear_passadis(m, n, self.amplada_entrada, self.num_entrades, entrada_unica, entrades_laterals)
    
    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades
    
    def get_amplada_entrada(self):
        return self.amplada_entrada

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