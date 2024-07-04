import simulacio as sim
import classe_passadis as cp
import time
import pygame

# Obté el tamany de la pantalla del dispositiu on s'executi el programa
pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w * 0.95
screen_height = screen_info.current_h * 0.95

# Crear una instància de la classe Passadis amb els paràmetres donats
"""
Paràmentres algorisme genètic
- Identificador únic del passadís (si només es crea un passadís pot ficar sempre 0)
- Valor de m (files)
- Valor de n (columnes)
- Amplada de la entrada (quanitat de cel·les que ocupa cada entrada quan entrada_unica és False)
- Entrada única: és una variable booleana que pot valdre True o False
- Entrades laterals: és una variable booleana que pot valdre True o False. Si entrada única es True no hi hauràn entrades laterals.
- Obstacles: és una variable booleana que pot valdre True o False
"""
passadis = cp.Passadis(0, 40, 25, 1, True, False, False)

# Executar l'algoritme genètic amb el passadís creat i els paràmetres donats
"""
Paràmentres algorisme genètic
- Passadís
- Nombre de iteracions de la simulació
- Aforament
- Fotogrames per segon
- Amplada de la pantalla
- Alçada de la pantalla
"""
sim.simulacio(passadis, 250, 400, 15, screen_width, screen_height)