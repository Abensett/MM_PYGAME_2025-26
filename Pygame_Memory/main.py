import pygame, sys
from pygame.locals import QUIT
import random
import os
import time

# SUR MAC UTILISER PYTHON 3.13 car problème de dépendances 

pygame.init()

# === Configuration de la fenêtre ===
largeur, hauteur = 1000, 1000
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption('Mon Memory Game Arcane')

# === Palette de couleurs ===
bleu = "#6B620E"    # couleur de fond
blanc = "#ffffff"   # couleur des cartes cachées

# === Configuration des cartes ===
carte_largeur = 200
carte_hauteur = 200
espacement_des_cartes = 10
nb_lignes = 4       # grille 4x4 = 16 cartes (8 paires)
nb_colonnes = 4

# === Liste des chemins vers les images ===
# Chaque image correspond à un personnage d'Arcane
images = [
    "./img/caitlyn.png",
    "./img/ekko.png",
    "./img/heimerdinger.png",
    "./img/jayce.png",
    "./img/jinx.png",
    "./img/silco.png",
    "./img/vi.png",
    "./img/viktor.png",
]

# === Génération des paires ===
# Calcule le nombre de paires nécessaires (16 cartes = 8 paires)
nombre_de_paires = (nb_lignes * nb_colonnes) // 2

# Crée une liste de valeurs uniques ("0" à "7")
nombres = [str(i) for i in range(nombre_de_paires)]

# Duplique chaque valeur pour créer les paires
paires = nombres * 2

# Mélange aléatoirement les paires
random.shuffle(paires)
print("Paires mélangées:", paires)

# === Chargement et redimensionnement des images ===
liste_images = []

for path in images:
    # Vérifie si le fichier existe
    if not os.path.exists(path):
        print(f"⚠️  Image manquante: {path}")
        
        # Crée un placeholder (carré gris avec bordure) si l'image manque
        placeholder = pygame.Surface((carte_largeur, carte_hauteur))
        placeholder.fill((230, 230, 230))
        pygame.draw.rect(placeholder, (100, 100, 100), placeholder.get_rect(), 2)
        liste_images.append(placeholder)
        continue

    # Charge l'image avec support de la transparence (PNG)
    img = pygame.image.load(path).convert_alpha()
    
    # Redimensionne l'image aux dimensions d'une carte
    img = pygame.transform.scale(img, (carte_largeur, carte_hauteur))
    
    liste_images.append(img)
    print(f"✅ Chargée: {os.path.basename(path)}")

# === Création de la grille de cartes ===
cartes = []

# Calcule l'espace total occupé par la grille
total_w = nb_colonnes * carte_largeur + (nb_colonnes - 1) * espacement_des_cartes
total_h = nb_lignes * carte_hauteur + (nb_lignes - 1) * espacement_des_cartes

# Calcule les offsets pour centrer la grille dans la fenêtre
offset_x = (largeur - total_w) // 2
offset_y = (hauteur - total_h) // 2

# Crée chaque carte avec sa position et sa valeur
for ligne in range(nb_lignes):
    for colonne in range(nb_colonnes):
        # Calcule la position (x, y) en pixels de la carte
        x = offset_x + colonne * (carte_largeur + espacement_des_cartes)
        y = offset_y + ligne * (carte_hauteur + espacement_des_cartes)

        # Crée un dictionnaire représentant la carte
        carte = {
            "valeur_carte": paires.pop(),                # valeur unique de la carte ("0" à "7")
            "dessin_carte": pygame.Rect(x, y, carte_largeur, carte_hauteur),  # rectangle de collision
            "carte_retournee": False,                    # état: face visible ou cachée
            "carte_identique": False,                    # True si la paire a été trouvée
        }
        cartes.append(carte)

# === Variables d'état du jeu ===
cartes_retournees = []  # stocke les 2 cartes en cours de comparaison (max 2)
paires_trouvees = 0     # compteur de paires validées (victoire à 8)

# === Boucle principale du jeu ===
running = True
while running:
    # Variables pour gérer les clics de cette frame
    click_detecte = False
    mouse_pos = None

    # === Gestion des événements (clavier, souris, fenêtre) ===
    for event in pygame.event.get():
        # Fermeture de la fenêtre (croix ou Alt+F4)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Détection du clic gauche (si le jeu n'est pas terminé)
        if event.type == pygame.MOUSEBUTTONDOWN and paires_trouvees < nombre_de_paires:
            click_detecte = True
            mouse_pos = pygame.mouse.get_pos()

    # === Logique de clic sur une carte ===
    if click_detecte and mouse_pos is not None:
        # Parcourt toutes les cartes pour trouver celle cliquée
        for carte in cartes:
            # Ignore les cartes déjà trouvées et vérifie si la souris est dessus
            if not carte["carte_identique"] and carte["dessin_carte"].collidepoint(mouse_pos):
                
                # Retourne la carte si elle est face cachée
                if not carte["carte_retournee"]:
                    carte["carte_retournee"] = True
                    cartes_retournees.append(carte)

                    # === Comparaison quand 2 cartes sont retournées ===
                    if len(cartes_retournees) == 2:
                        # Affiche d'abord les 2 cartes retournées
                        fenetre.fill(bleu)
                        for c in cartes:
                            if c["carte_retournee"]:
                                index = int(c["valeur_carte"])
                                fenetre.blit(liste_images[index], c["dessin_carte"])
                            else:
                                pygame.draw.rect(fenetre, blanc, c["dessin_carte"])
                        pygame.display.update()
                        
                        # Pause pour laisser voir les cartes (800ms)
                        time.sleep(0.8)
                        
                        # Compare les valeurs
                        c1, c2 = cartes_retournees
                        
                        if c1["valeur_carte"] == c2["valeur_carte"]:
                            # Paire trouvée: marque les cartes comme identiques
                            c1["carte_identique"] = True
                            c2["carte_identique"] = True
                            paires_trouvees += 1
                        else:
                            # Pas identiques: recache les cartes
                            c1["carte_retournee"] = False
                            c2["carte_retournee"] = False
                        
                        # Réinitialise la sélection pour le prochain tour
                        cartes_retournees = []
                
                # Sort de la boucle après avoir traité une carte (évite multi-clics)
                break

    # === Rendu graphique ===
    # Efface l'écran avec le fond bleu
    fenetre.fill(bleu)

    # Dessine chaque carte selon son état
    for carte in cartes:
        if carte["carte_retournee"]:
            # Carte face visible: affiche l'image du personnage
            index = int(carte["valeur_carte"])
            fenetre.blit(liste_images[index], carte["dessin_carte"])
        else:
            # Carte face cachée: dessine un rectangle blanc
            pygame.draw.rect(fenetre, blanc, carte["dessin_carte"])

    # Affiche la frame à l'écran
    pygame.display.update()