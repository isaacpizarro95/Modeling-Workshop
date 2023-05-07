import simulacio_2D as s2D
import time

# Recordem el prototip de la funció simulacio_2D:
#   simulacio_2D(id_passadis, m, n, num_iteracions, aforament, entrada_unica=False, entrades_laterals=False)
        # id_passadis = identificador de cada objecte 'passadís'
        # m = nombre de files del passadís
        # n = nombre de columnes/carrils del passadís
        # num_iteracions = "temps" que dura la simulació abans de parar
        # aforament = capacitat màxima que pot tenir el passadís
        # entrada_unica = True si tota la part de dalt i abaix és entrada, False si no és així
        # entrades_laterals = True si hi han entrades a les parets laterals, False si no és així

# Cadena de simulacions
# s2D.simulacio_2D(0, 40, 10, 20, 30) # Passadís 10*10, normal i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(1, 10, 10, 20, 30, False, True) # Passadís 10*10, amb entrades laterals i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(2, 10, 20, 20, 30, True) # Passadís 10*10, amb entrada única i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(3, 10, 20, 20, 40, True) # Passadís 10*20 amb entrada única i aforo = 40
# time.sleep(3)
# s2D.simulacio_2D(4, 10, 20, 20, 100, True) # Passadís 10*20 amb entrada única i aforo = 100
# time.sleep(3)
# s2D.simulacio_2D(5, 10, 6, 20, 40, True) # passadís 10*6 amb entrada única i aforo = 40
# time.sleep(3)
s2D.simulacio_2D(6, 30, 40, 60, 100, True) # Passadís 30*40 amb entrada única i aforo = 100

#s2D.simulacio_2D(0, 10, 10, 30, 30)