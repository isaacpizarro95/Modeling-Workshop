import random
import utils_passadis as up

# Classe Passadís en el model Discret
class Passadis:

    # Inicialització de la classe Passadís
    def __init__(self, id, m, n, amplada_entrada = 1, entrada_unica=True, entrades_laterals=False, obstacles=False):
        # Identificador únic del passadís per diferenciar-lo
        self.id = id

        # Nombre de files
        self.m = m

        # Nombre de carrils (columnes)
        self.n = n

        # Número que determina quantes cel·les ocupa cada accés (entrada/sortida)
        self.amplada_entrada = amplada_entrada

        # True => totes les cel·les de la primera i ultima fila son entrada
        self.entrada_unica = entrada_unica    

        # True => hi han entrades també a les parets laterals
        self.entrades_laterals = entrades_laterals

        # True => hi ha obstacles al passadís
        self.obstacles = obstacles                          
            
        # Si entrada_unica és False aquesta variable determina quants accesos poden crearse
        self.num_entrades = random.randint(m//amplada_entrada, ((2*(n+m))-4)//amplada_entrada)

        # Creació de la matriu i obtenció de les posicions de entrades, parets i obstacles
        self.passadis, self.entrades, self.parets, self.obstacles = up.crear_passadis(m, n, self.amplada_entrada, self.num_entrades, entrada_unica, entrades_laterals, obstacles)

        # Llista dels individus que es troben al passadís
        self.ind_in_passadis = []

        # Diccionari que conté la posició de cada individu
        self.diccionario_posicion = {}                       
    
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

    # Retorna l'amplada de l'entrada
    def get_amplada_entrada(self):
        return self.amplada_entrada                         

    # Retorna el nombre d'entrades
    def get_num_entrades(self):
        return self.num_entrades                            

    # Retorna si l'entrada és única o no
    def get_entrada_unica(self):
        return self.entrada_unica                           

    # Retorna les parets
    def get_parets(self):
        return self.parets                                  

    # Retorna els obstacles
    def get_obstacles(self):
        return self.obstacles                               

    # Retorna la matriu que conté el passadís
    def get_passadis(self):
        return self.passadis                                

    # Retorna els individus que es troben al passadís
    def get_ind_in_passadis(self):
        return self.ind_in_passadis                         

    # Retorna el diccionari de posicions
    def get_diccionario_posicion(self):
        return self.diccionario_posicion                    












# # Classe Passadís en el model Discret
# class Passadis:
#     def __init__(self, id, m, n, mod = 'defecte', amplada_entrada = 1, entrada_unica=False, entrades_laterals=False, obstacles=False):
#         self.id = id                                        # identificador únic del passadís per diferenciar-lo
#         self.m = m                                          # m files
#         self.n = n                                          # n carrils (columnes)
#         self.amplada_entrada = amplada_entrada              # enter que determina quantes cel·les ocupa cada entrada
#         self.entrada_unica = entrada_unica                  # True si tot es entrada o False si hi han entrades concretes
#         self.entrades_laterals = entrades_laterals          # True si poden haver entrades als laterals del passadís
#         self.obstacles = obstacles                          # True si posem obstacles i False si no. Podem afegir un altra variable per descriure els obstacles
#         self.num_entrades = 0
#         self.mod = mod

#         if mod == 'defecte':              
#             if entrada_unica == True:
#                 self.num_entrades = random.randint(n//amplada_entrada, ((2*n)-4)//amplada_entrada)  
#             else: self.num_entrades = random.randint(m//amplada_entrada, ((2*(n+m))-4)//amplada_entrada)

#         elif mod == 'coll_ampolla':
#             self.num_entrades = n+1 # n-2 entrades per la entrada gran i 3 entrades per la sortida

#         # Creació del passadís
#         self.passadis, self.entrades, self.parets, self.obstacles = up.crear_passadis(m, n, mod, self.amplada_entrada, self.num_entrades, entrada_unica, entrades_laterals, obstacles)

#         self.ind_in_passadis = []
#         self.diccionario_posicion = {}
    

#     def get_id(self):
#         return self.id

#     def get_m(self):
#         return self.m

#     def get_n(self):
#         return self.n

#     def get_mod(self):
#         return self.mod
    
#     def get_entrades(self):
#         return self.entrades

#     def get_amplada_entrada(self):
#         return self.amplada_entrada
        
#     def get_num_entrades(self):
#         return self.num_entrades

#     def get_entrada_unica(self):
#         return self.entrada_unica
    
#     def get_entrades_laterals(self):
#         return self.entrades_laterals

#     def get_parets(self):
#         return self.parets
    
#     def get_obstacles(self):
#         return self.obstacles

#     def get_passadis(self):
#         return self.passadis
    
#     def get_ind_in_passadis(self):
#         return self.ind_in_passadis
    
#     def get_diccionario_posicion(self):
#         return self.diccionario_posicion