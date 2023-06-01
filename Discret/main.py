import simulacio as s2D
import classe_passadis as cp

cas1 = cp.Passadis(0, 30, 15, 'defecte', 6, True, False, False)
s2D.simulacio_2D(cas1, 300, 100)

# cas2 = cp.Passadis(0, 30, 20, 'coll_ampolla', 3, True, False, False)
# s2D.simulacio_2D(cas2, 200, 100)

# cas3 = cp.Passadis(0, 40, 30, 'defecte', 3, True, False, True)
# s2D.simulacio_2D(cas3, 200, 500)

# Cadena de simulacions
# s2D.simulacio_2D(0, 40, 10, 20, 30) # Passadís 10*10, normal i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(1, 10, 10, 20, 30, False, True) # Passadís 10*10, amb entrades laterals i aforo = 30
# time.sleep(3)
#s2D.simulacio_2D(2, 20, 14, 30, 30, True) # Passadís 10*10, amb entrada única i aforo = 30
# time.sleep(3)
# s2D.simulacio_2D(3, 10, 20, 20, 40, True) # Passadís 10*20 amb entrada única i aforo = 40
# time.sleep(3)
# s2D.simulacio_2D(4, 10, 20, 20, 100, True) # Passadís 10*20 amb entrada única i aforo = 100
# time.sleep(3)
# s2D.simulacio_2D(5, 10, 6, 20, 40, True) # passadís 10*6 amb entrada única i aforo = 40
# time.sleep(3)
#s2D.simulacio_2D(6, 30, 40, 60, 100, True) # Passadís 30*40 amb entrada única i aforo = 100

#s2D.simulacio_2D(0, 10, 10, 30, 30)