import random
import utils_passadis as up

# En aquest fitxer configurem els diferents passadissos
# Classe Passadís en el model Continu
class Passadis:
    def __init__(self, id, m, n):
        self.id = id
        self.m = m
        self.n= n
        self.ind_in_passadis = []
        self.ind_posicions = {}

        self.entrades, self.parets = up.crear_passadis(m, n)

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n
    
    def get_entrades(self):
        return self.entrades

    def get_parets(self):
        return self.parets
    
    def get_ind_in_passadis(self):
        return self.ind_in_passadis

    def get_ind_posicions(self):
        return self.ind_posicions
    
    # def get_obstacles(self):
    #     return self.obstacles