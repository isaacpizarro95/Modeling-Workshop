import simulacio as sim
import config_passadis as cp

"""
Quant més petit és escalat pixel més grans podem fer els passadissos.
Es recomana mantenir l'escalat per sobre de 30 per a una bona representació.

Es recomana mantenir m entre [5, 45]
Es recomana mantenir n entre [10, 35]
"""

 # Unitat de tamany base dels píxels de la simulació
escalat_pixel = 40

# Fotogrames per segon de la simulació
fps = 15

# Durada de la simulació i quantitat màxima d'individus en el passadís
iteracions = 1000
aforament = 100

# Creació del passadís
passadis = cp.Passadis(0, 15, 25)

# Executem la simulació
sim.simulacio(passadis, iteracions, aforament, escalat_pixel, fps)