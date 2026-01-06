import pygame, sys
from pygame.locals import QUIT
import math

pygame.init()

fenetre = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Visage arc-en-ciel! ")

FPS = 60
horloge = pygame.time.Clock()

# Compteur de frames (augmente de 1 à chaque image)
temps = 0

# 7 couleurs pour l'arc-en-ciel
couleurs = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]


def dessiner():
    global temps
    
    # Fond qui change de couleur toutes les 30 frames (0.5 sec)
    # temps // 30 → change de valeur toutes les 30 frames (0→0→...→0→1→1→...→1→2...)
    # % 7 → fait boucler entre 0 et 6 (les 7 couleurs)
    couleur_actuelle = couleurs[(temps // 30) % 7]
    fenetre.fill(couleur_actuelle)

    # Visage (rectangle blanc fixe)
    pygame.draw.rect(fenetre, "white", (50, 10, 200, 250))

    # Yeux qui clignent toutes les 2 secondes (120 frames)
    # temps % 120 → donne 0,1,2...119, puis recommence à 0
    # < 5 → ferme les yeux pendant les 5 premières frames (clignement rapide)
    if temps % 120 < 5:
        # Yeux fermés (lignes horizontales)
        pygame.draw.line(fenetre, "black", (185, 60), (215, 60), 3)
        pygame.draw.line(fenetre, "black", (85, 60), (115, 60), 3)
    else:
        # Yeux ouverts (cercles)
        pygame.draw.circle(fenetre, "black", (200, 60), 30, 3)
        pygame.draw.circle(fenetre, "black", (100, 60), 30, 3)
        
        # Pupilles qui tournent en cercle (rayon 8 pixels)
        # temps * 0.05 → angle qui augmente lentement (1 tour complet en ~2 sec)
        # cos → position gauche/droite (-8 à +8)
        # sin → position haut/bas (-8 à +8)
        pupille_x = int(8 * math.cos(temps * 0.05))
        pupille_y = int(8 * math.sin(temps * 0.05))
        
        pygame.draw.circle(fenetre, "black", (200 + pupille_x, 60 + pupille_y), 10)
        pygame.draw.circle(fenetre, "black", (100 + pupille_x, 60 + pupille_y), 10)

    # Nez (ligne verticale fixe)
    pygame.draw.line(fenetre, "black", (150, 120), (150, 150), 4)

    # Bouche qui alterne toutes les secondes (60 frames)
    # temps // 60 → change toutes les 60 frames (1 seconde)
    # % 2 → alterne entre 0 et 1 (pair/impair)
    if (temps // 60) % 2 == 0:
        # Expression 1: Sourire
        pygame.draw.ellipse(fenetre, "red", (80, 170, 140, 70))
    else:
        # Expression 2: Surprise (bouche en O)
        pygame.draw.ellipse(fenetre, "red", (120, 180, 60, 50))

    # Sourcils qui montent et descendent (oscillation)
    # sin fait des vagues entre -1 et +1
    # * 5 → amplitude de 5 pixels (-5 à +5)
    sourcil = int(5 * math.sin(temps * 0.1))
    pygame.draw.line(fenetre, "black", (70, 30 + sourcil), (130, 35), 3)
    pygame.draw.line(fenetre, "black", (170, 35), (230, 30 - sourcil), 3)

    # 3 étoiles qui tournent autour du visage (rayon 120 pixels)
    for i in range(3):
        # i * 2.1 → espace les 3 étoiles régulièrement (120° entre chaque)
        angle = temps * 0.05 + i * 2.1
        
        # Position sur le cercle (centre 150, 130)
        x = int(150 + 120 * math.cos(angle))
        y = int(130 + 120 * math.sin(angle))
        
        pygame.draw.circle(fenetre, "gold", (x, y), 5)

    pygame.display.update()


# Boucle principale
while True:
    # quit pygame et le programme lorsquque l'event QUIT est reçu cad clique sur la croix 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    dessiner()
    
    # Augmente le compteur de 1 à chaque frame
    temps += 1
    
    # Régule à 60 images/seconde
    horloge.tick(FPS)