import pygame, sys
from pygame.locals import QUIT
import time

pygame.init()  # lance Pygame

# crée la fenêtre (surface où dessiner)
fenetre = pygame.display.set_mode((400, 300))

FPS = 60  # cible d'images par seconde
horloge = pygame.time.Clock()  # pour réguler la boucle

pygame.display.set_caption("Hello World!")  # titre de la fenêtre


# Fonction pour les dessins / différentes méthodes applicables sur la fenêtre de jeu
def dessiner():
    # fill: remplit toute la surface avec une couleur → "efface" l'ancienne frame
    # Surface.fill(couleur) ; peut aussi prendre un rect pour ne remplir qu'une zone
    fenetre.fill("yellow")

    # draw.rect: dessine un rectangle (plein par défaut, width>0 = contour)
    # pygame.draw.rect(surface, couleur, (x, y, w, h), width=0, border_radius=0)
    fenetre.fill("yellow")
    pygame.draw.rect(fenetre, "white", (50, 10, 200, 250))  # plein, donc width par défaut

    # draw.circle: dessine un cercle (centre, rayon). width>0 = juste le contour
    # pygame.draw.circle(surface, couleur, (cx, cy), rayon, width=0)
    pygame.draw.circle(fenetre, "black", (200, 60), 30, 3)  # oeil droit: contour 3 px
    pygame.draw.circle(fenetre, "black", (100, 60), 30, 3)  # oeil gauche: contour 3 px

    # draw.line: trace une ligne entre 2 points (épaisseur avec width)
    # pygame.draw.line(surface, couleur, (x1, y1), (x2, y2), width=1)
    pygame.draw.line(fenetre, "black", (150, 120), (150, 150), 4)  # nez: ligne verticale épaisse

    # draw.ellipse: ellipse inscrite dans le rect donné (x, y, w, h)
    # pygame.draw.ellipse(surface, couleur, (x, y, w, h), width=0)
    pygame.draw.ellipse(fenetre, "red", (80, 170, 140, 70))  # bouche: pleine (width=0)

    # affiche tout d'un coup à la fin du dessin (une seule fois par frame)
    pygame.display.update()


# boucle principale
while True:
    debut_frame = time.time()  # mesure la durée de la frame

    # gère les événements (fermeture fenêtre, etc.)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # dessine la scène
    dessiner()

    # régule le framerate et log la durée réelle
    horloge.tick(FPS)
    print("Durée en secondes :", time.time() - debut_frame)