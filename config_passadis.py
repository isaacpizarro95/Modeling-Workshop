import random
import utils_passadis as up

# En aquest fitxer configurem els diferents passadissos
class Pasillo:
    def __init__(self, id, m, n, amplada_entrada=1, entrada_unica=False, entrades_laterals=False, obstacles=False):
        self.id = id
        self.m = m
        self.n= n
        self.amplada_entrada = amplada_entrada
        self.entrada_unica = entrada_unica
        self.entrades_laterals = entrades_laterals
        self.obstacles = obstacles
        self.ind_en_passadis = []
        #self.diccionario_posicion = {}

        self.num_entrades = 0
        if entrada_unica == True:
            self.num_entrades = random.randint(n//amplada_entrada, ((2*n)-4)//amplada_entrada)  
        else: self.num_entrades = random.randint(m//amplada_entrada, ((2*(n+m))-4)//amplada_entrada)

        self.passadis, self.entrades, self.parets, self.obstacles = up.crear_passadis(m, n, amplada_entrada, self.num_entrades, entrada_unica, entrades_laterals, obstacles)

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
    
    def get_obstacles(self):
        return self.obstacles

    def get_passadis(self):
        return self.passadis
    
    def get_ind_in_passadis(self):
        return self.ind_in_passadis
    
    # def get_diccionario_posicion(self):
    #     return self.diccionario_posicion