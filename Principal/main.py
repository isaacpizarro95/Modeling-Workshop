import simulacio_2D as s2D
import config_passadis as cp
import time

# Recordem el que necessitem:
        # Passadis:
                # id
                # m (llargada passadis)
                # n (amplada passadis(carrils))
                # amplada_entrada (quantes cel·les ocupa cada entrada). Per defecte = 1
                # entrada_unica (si tota la part inferior i superior son entrades). Per defecte = False
                # entrades_laterals (si hi han entrades als laterals). Per defecte = False
                # obstacles (si hi han obstacles o no al mapa). Per defecte = False
        # Simulació:
                # passadís
                # nombre d'iteracions (valor màxim de t)
                # aforo màxim al passadís

# Cadena de simulacions
#Passadís 8*2, entrada_unica = True, 30 iteracions, 6 aforo 
cas1 = cp.Passadis(0, 15, 6, 3, True)
s2D.simulacio_2D(cas1, 20, 10)
time.sleep(1.5)

# #Passadís 16*8, amplada_entrada = 2, 30 iteracions, 20 aforo 
# cas2 = cp.Passadis(1, 18, 10, 2)
# s2D.simulacio_2D(cas2, 30, 20)
# time.sleep(1.5)

# # Passadís 18*8, amplada_entrada = 3, entrades_laterals = True, 30 iteracions, 30 aforo
# cas3 = cp.Passadis(2, 20, 10, 3, False, True)
# s2D.simulacio_2D(cas3, 30, 30)
# time.sleep(1.5)

# #Passadís 18*14, entrada_unica = True, 30 iteracions, 40 aforo 
# cas4 = cp.Passadis(3, 20, 16, 1, True)
# s2D.simulacio_2D(cas4, 30, 40)
# time.sleep(1.5)

# # Passadís 40*30, entrades_laterals = True, 80 iteracions, 80 aforo
# cas5 = cp.Passadis(4, 42, 32, 6, False, True)
# s2D.simulacio_2D(cas5, 80, 80)
# time.sleep(1.5)

