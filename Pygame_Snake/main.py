import pygame, sys
from pygame.locals import QUIT
import random
import os

pygame.init()

# Initialise le mixer (pour jouer un son)
try:
    pygame.mixer.init()
    audio_ok = True
except pygame.error:
    audio_ok = False

# fenêtre de jeu
largeur, hauteur = 800, 500
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption('NOKIA 3310')

# couleurs (fond sombre, serpent vert néon, pion rouge vif)
noir = "#1A1A2E"
vert_neon = "#0FFF50"
rouge_vif = "#FF006E"

# grille: taille d'une cellule + nb de cellules en X/Y
cellule = 20
nb_cellule_x = largeur // cellule
nb_cellule_y = hauteur // cellule

# horloge pour contrôler la vitesse (ticks/seconde)
horloge = pygame.time.Clock()

# directions possibles (dx, dy)
haut = (0, -1)
bas = (0, 1)
gauche = (-1, 0)
droite = (1, 0)

# charge le son si possible
son_jeu = None
if audio_ok:
    son_path = os.path.join('music.mp3')
    if os.path.exists(son_path):
        son_jeu = pygame.mixer.Sound(son_path)

# (ré)initialise l'état du jeu (serpent/direction/pion)
def depart_serpent():
    # joue la mélodie au (re)démarrage si dispo
    if son_jeu:
        son_jeu.stop()
        son_jeu.play()

    # serpent de 3 segments, tête à gauche (orientation vers la droite)
    snake = [(9, 5), (8, 5), (7, 5)]
    direction = droite
    pion = (random.randint(0, nb_cellule_x - 1), random.randint(0, nb_cellule_y - 1))

    return snake, direction, pion

# initialise une première fois
snake, direction, pion = depart_serpent()

# boucle de jeu principale
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # change la direction si pas l'inverse (évite demi-tour immédiat)
            if event.key == pygame.K_UP and direction != bas:
                direction = haut
            elif event.key == pygame.K_DOWN and direction != haut:
                direction = bas
            elif event.key == pygame.K_LEFT and direction != droite:
                direction = gauche
            elif event.key == pygame.K_RIGHT and direction != gauche:
                direction = droite

    # déplacement du serpent
    x_tete, y_tete = snake[0]
    x = x_tete + direction[0]
    y = y_tete + direction[1]
    snake.insert(0, (x, y))

    # collisions (bords ou soi-même)
    out_of_bounds = (x < 0 or x >= nb_cellule_x) or (y < 0 or y >= nb_cellule_y)
    self_collision = snake.count((x, y)) > 1
    if out_of_bounds or self_collision:
        if son_jeu:
            son_jeu.stop()
        snake, direction, pion = depart_serpent()

    # a-t-on mangé le pion ?
    if (x, y) == pion:
        pion = (random.randint(0, nb_cellule_x - 1), random.randint(0, nb_cellule_y - 1))
    else:
        snake.pop()

    # dessin de la frame (fond)
    fenetre.fill(noir)

    # dessine le serpent: chaque segment = un carré vert néon
    for segment in snake:
        seg_x, seg_y = segment
        pygame.draw.rect(
            fenetre,
            vert_neon,
            (seg_x * cellule, seg_y * cellule, cellule, cellule)
        )

    # dessine le pion rouge vif
    pygame.draw.rect(
        fenetre,
        rouge_vif,
        (pion[0] * cellule, pion[1] * cellule, cellule, cellule)
    )

    # vitesse du jeu: 5 ticks/s
    horloge.tick(5)

    # affiche le backbuffer
    pygame.display.update()