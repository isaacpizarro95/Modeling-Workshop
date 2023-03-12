import numpy as np

# En aquest fitxer configurem els diferents passadissos
# Per simplificar la majoria de variables (potser totes) no podran ser modificades un cop creat el passadis
class Passadis:
    def __init__(self, id, m_llarg, n_carrils, dif_entrades, k_entrades, obstacles):
        self.id = id                        # identificador únic del passadís per diferenciar-lo
        self.m_llarg = m_llarg              # m files
        self.n_carrils = n_carrils          # n carrils (columnes)
        self.dif_entrades = dif_entrades    # 1 si diferenciem entre entrades i sortides i 0 si no 
        self.k_entrades = k_entrades        # k entrades (si dif_entrades == 1 tambe hi hauran k sortides)
        self.obstacles = obstacles          # 1 si posem obstacles i 0 si no. Podem afegir un altra variable per descriure els obstacles
        self.passadis = np.zeros((m_llarg, n_carrils)) # creem la matriu que contindrà el nostre passadís

    def get_id(self):
        return self.id

    def get_m(self):
        return self.m_llarg

    def get_n(self):
        return self.n_carrils
    
    def get_dif_entrades(self):
        return self.dif_entrades
    
    def get_k(self):
        return self.k_entrades

    def get_passadis(self):
        return self.passadis
    
    def get_entrades(self):
        # Les entrades dels carrils que van en direcció cap a dalt son de la forma (m-1, j) 0 <= j <= n
        # Les sortides dels carrils que van en direcció cap a dalt son de la forma (0, j) 0 <= j <= n

        # Les entrades dels carrils que van en direcció cap a baix son de la forma (0, j) 0 <= j <= n
        # Les sortides dels carrils que van en direcció cap a baix son de la forma (m-1, j) 0 <= j <= n

        # Si j és parell la direcció serà cap a dalt i si és senar cap a baix
        entradas = []
        salidas = []
        for j in range(self.n_carrils):
            if j % 2 == 0:
                entradas.append((self.m_llarg-1, j))
                salidas.append((0, j))
            else:
                entradas.append((0, j))
                salidas.append((self.m_llarg, j))
        return (entradas, salidas)