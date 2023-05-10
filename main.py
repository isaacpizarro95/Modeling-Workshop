#import Genetic.simulacio as s2D
import simulacio_2D as s2D
import config_passadis as cp
#import time

cas1 = cp.Passadis(0, 35, 28, 3, True, False, False)
s2D.simulacio_2D(cas1, 100, 200)

# Cadena de simulacions
# s2D.simulacio_2D(0, 40, 10, 20, 30) # Passadís 10*10, normal i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(1, 10, 10, 20, 30, False, True) # Passadís 10*10, amb entrades laterals i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(2, 20, 14, 30, 30, True) # Passadís 10*10, amb entrada única i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(3, 10, 20, 20, 40, True) # Passadís 10*20 amb entrada única i aforo = 40
# time.sleep(3)
# s2D.simulacio_2D(4, 10, 20, 20, 100, True) # Passadís 10*20 amb entrada única i aforo = 100
# time.sleep(3)
# s2D.simulacio_2D(5, 10, 6, 20, 40, True) # passadís 10*6 amb entrada única i aforo = 40
# time.sleep(3)
# s2D.simulacio_2D(6, 30, 40, 60, 100, True) # Passadís 30*40 amb entrada única i aforo = 100
# s2D.simulacio_2D(0, 10, 10, 30, 30)