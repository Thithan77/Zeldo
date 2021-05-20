import random
import pygame
from pygame.locals import *
pygame.init()

def main(fen):

    var=True
    fond=pygame.image.load("C:assets\\noir.jpg").convert_alpha()
    font=pygame.font.Font("C:assets\\akbar.ttf", 30)
    while var:
        for e in pygame.event.get():
            if (e.type==QUIT):
                var=False
        fen.blit(fond,(0,0))
        pygame.display.flip()

        winner = None
        player_health = 100
        enemy=0

        while enemy==0:
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if (e.key==K_1) or (e.key==K_KP1):
                        afficher = font.render("Ennemi choisi !", 1, (255, 255, 255))
                        fen.blit(choix_ennemi, (130,130))
                        pygame.display.flip()
                        enemy="1"
                choix_ennemi = font.render("Choisissez votre ennemi : 1. Squelette", 1, (255, 255, 255))
                fen.blit(choix_ennemi, (2,130))
                pygame.display.flip()
                

        if enemy in ("1", "Squelette"):
            computer_health = 50
            
        # On détermine c'est le tour de qui
        turn = random.randint(1,2) # Pile ou face
        if turn == 1:
            player_turn = True
            computer_turn = False
            print("\nC'est votre tour.")
        else:
            player_turn = False
            computer_turn = True
            print("\nC'est le tour de votre adversaire.")

        print("\nVotre vie: ", player_health, "Vie de l'adversaire: ", computer_health)

        # On prépare la boucle principale
        while (player_health != 0 or computer_health != 0):
            heal_up = False # Détermine si le soin est utlisé par le joueuur. Se remmet en faux à chaque boucle.

            # Crée un dictionnaire des mouvements possibles et choisi aléatoirement les dégats/soins effectués.
            moves = {"Punch": random.randint(10, 15),
                     "Mega Punch": random.randint(12, 17),
                     "Heal": random.randint(10, 15),
                     "Little Punch": random.randint(7, 12)}

            if player_turn:
                print("\nSelectionnez une attaque:\n1. Coup de Poing (Faire entre 10 à 15 points de dégats)\n2. Méga Coup de Poing (Faire entre 12 à 17 points de dégats (Plus de chance de rater))\n3. Soin (Soigne entre 10 et 15 points de vie)\n")

                player_move = input("> ").lower()

                if player_move in ("1", "poing","coup de poing"):
                    move_miss = random.randint(1,10) # 10% de chance de rater
                    if move_miss == 1:
                        player_move = 0 # Le joueur rate et fait 0 dégats
                        print("Vous avez raté !")
                    else:
                        player_move = moves["Punch"]
                        print("\nVous donnez un coup de poing. Cela fait ", player_move, " dégâts.")
                elif player_move in ("2", "mega poing","mega coup de poing"):
                    move_miss = random.randint(1,5) # 20% de chance de rater
                    if move_miss == 1:
                        player_move = 0 # Le joueur rate et fait 0 dégats
                        print("Vous avez raté !")
                    else:
                        player_move = moves["Mega Punch"]
                        print("\nVous donnez un méga coup de poing. Cela fait ", player_move, " dégâts.")
                elif player_move in ("3", "soin"):
                    heal_up = True # Soin activé
                    player_move = moves["Heal"]
                    print("\nVous vous soignez de", player_move, " points de vie.")
                else:
                    print("\nCe n'est pas un choix correct. Réessayez.")
                    continue

            else: # Tour de l'adversaire
                if enemy in ("1", "squelette") :
                    move_miss = random.randint(1,7)
                    if move_miss == 1:
                        miss = True
                    else:
                        miss = False

                    if miss:    
                        computer_move = 0 # L'adversaire rate et fait 0 dégats
                        print("Votre adversaire a raté son attaque !")
                    else:
                        computer_move = moves["Little Punch"]
                        print("\nVotre adversaire vous donne un petit coup de poing. Cela fait ", computer_move, " dégats.")

            if heal_up:
                player_health += player_move
                if player_health > 100:
                    player_health = 100 # PV maximum de 100!
            else:
                if player_turn:
                    computer_health -= player_move
                    if computer_health <= 0:
                        computer_health = 0 # PV minimum de 0.
                        winner = "Player"
                        break
                else:
                    player_health -= computer_move
                    if player_health < 0:
                        player_health = 0
                        winner = "Computer"
                        break

            print("\nVos PV: ", player_health, "PV de l'adversaire: ", computer_health)

            # Changement de tour
            player_turn = not player_turn
            computer_turn = not computer_turn

        # Une fois que la boucle principale est terminée, on détermine le gagnant.

        if winner == "Player":
            print("\nVos PV: ", player_health, "PV de l'adversaire: ", computer_health)
            print("\nVictoire !")
        else:
            print("\nVos PV: ", player_health, "PV de l'adversaire: ", computer_health)
            print("\nDéfaite !")
        var=0