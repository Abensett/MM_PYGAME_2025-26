import pygame, sys
from pygame.locals import *


def main():
    pygame.init()

    # fenetre 600x600, grille de 12x12 cases
    largeur, hauteur = 600, 600
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption('Mon labyrinthe !')

    fond = "#1a1a2e"            # bleu nuit
    mur_couleur = "#e94560"     # rouge vif
    joueur_couleur = "#0f3460"  # bleu fonce
    arrivee_couleur = "#c1ffa0" # vert clair

    # chaque case fait 50 pixels
    cellule = 50

    # les murs : chaque tuple c'est (colonne, ligne) sur la grille
    murs = [
        (2, 1), (3, 1), (4, 1), (5, 1),
        (1, 3), (1, 4), (1, 5), (1, 6),
        (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
        (8, 2), (8, 3), (8, 4), (8, 5),
        (3, 7), (4, 7), (5, 7),
        (6, 8), (6, 9), (6, 10),
        (9, 7), (10, 7), (10, 8), (10, 9),
    ]

    # le joueur demarre en haut a gauche
    joueur_x = 0
    joueur_y = 0

    # police pour afficher du texte (None = police par defaut, 48 = taille en pixels)
    font = pygame.font.Font(None, 48)

    # l'arrivee c'est la derniere case en bas a droite
    # 600 / 50 = 12 cases, donc la derniere c'est l'index 11
    arrivee_col = (largeur // cellule) - 1
    arrivee_lig = (hauteur // cellule) - 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # a chaque appui sur une fleche on bouge d'une case
            # on check qu'on sort pas de l'ecran
            if event.type == KEYDOWN:
                if event.key == K_LEFT and joueur_x > 0:
                    joueur_x -= cellule
                elif event.key == K_RIGHT and joueur_x < largeur - cellule:
                    joueur_x += cellule
                elif event.key == K_UP and joueur_y > 0:
                    joueur_y -= cellule
                elif event.key == K_DOWN and joueur_y < hauteur - cellule:
                    joueur_y += cellule

        # on convertit la position du joueur (pixels) en position sur la grille
        # division entiere : 150 // 50 = case 3
        col = joueur_x // cellule
        lig = joueur_y // cellule

        # si la case du joueur est dans la liste des murs -> perdu
        if (col, lig) in murs:
            texte = font.render("GAME OVER", True, mur_couleur)
            fenetre.blit(texte, (largeur // 2 - texte.get_width() // 2, hauteur // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # si le joueur est sur la case d'arrivee -> gagne
        if col == arrivee_col and lig == arrivee_lig:
            texte = font.render("VICTOIRE !", True, arrivee_couleur)
            fenetre.blit(texte, (largeur // 2 - texte.get_width() // 2, hauteur // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # on efface tout puis on redessine a chaque frame
        fenetre.fill(fond)

        # les murs : on convertit les coords grille en pixels (* cellule)
        for mur in murs:
            pygame.draw.rect(fenetre, mur_couleur, (mur[0] * cellule, mur[1] * cellule, cellule, cellule))

        # le carre vert d'arrivee en bas a droite
        pygame.draw.rect(fenetre, arrivee_couleur, (arrivee_col * cellule, arrivee_lig * cellule, cellule, cellule))

        # le joueur est deja en pixels donc on le dessine direct
        pygame.draw.rect(fenetre, joueur_couleur, (joueur_x, joueur_y, cellule, cellule))

        # on affiche tout ce qu'on a dessine
        pygame.display.update()


# le jeu se lance que si on execute ce fichier directement
# si on l'importe depuis un autre fichier, ca se lance pas -> prendre l'habitude de faire ça avec les makers
if __name__ == "__main__":
    main()