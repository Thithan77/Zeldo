import random
import pygame
from pygame.locals import *
pygame.init()

def main(fen):

    var=True
    fond=pygame.Surface(fen.get_size())
    font=pygame.font.Font("assets\\akbar.ttf", 30)
    fond = fond.convert()
    fond.fill((0,0,0))

    for e in pygame.event.get():
        if (e.type==QUIT):
            var=False
    fen.blit(fond,(0,0))
    pygame.display.flip()

    winner = None
    player_health = 100
    enemy=0

    while enemy==0:
        choix_ennemi = font.render("Choisissez votre ennemi : 1. Squelette", 1, (255, 255, 255))
        fen.blit(fond,(0,0))
        fen.blit(choix_ennemi, (150,30))
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if (e.key==K_1) or (e.key==K_KP1):
                    afficher = font.render("Ennemi choisi !", 1, (255, 255, 255))
                    fen.blit(fond,(0,0))
                    fen.blit(afficher, (150,30))

                    enemy="1"
            pygame.display.flip()       

    if enemy=="1":
        computer_health = 50
            
    # On détermine c'est le tour de qui
    turn = random.randint(1,2) # Pile ou face
    if turn == 1:
        player_turn = True
        computer_turn = False
        tour=font.render("C'est votre tour.", 1, (255, 255, 255))
        fen.blit(tour, (150,80))
        pygame.display.flip() 
    else:
        player_turn = False
        computer_turn = True
        tour=font.render("C'est le tour de votre adversaire.", 1, (255, 255, 255))
        fen.blit(tour, (150,80))
        pygame.display.flip() 

    vie=font.render("Votre vie: "+str(player_health)+"   Vie de l'adversaire: "+str(computer_health), 1, (255,255,255))
    fen.blit(vie, (150,130))
    pygame.display.flip()

    # On prépare la boucle principale
    while (player_health != 0 or computer_health != 0):
        heal_up = False # Détermine si le soin est utlisé par le joueuur. Se remmet en faux à chaque boucle.

        # Crée un dictionnaire des mouvements possibles et choisi aléatoirement les dégats/soins effectués.
        moves = {"Punch": random.randint(10, 15),
                 "Mega Punch": random.randint(12, 17),
                 "Heal": random.randint(10, 15),
                 "Little Punch": random.randint(7, 12)}

        if player_turn:
            choix_attaque1=font.render("Selectionnez une attaque:",1,(255,255,255))
            choix_attaque2=font.render("1. Coup de Poing (Entre 10 et 15 degats, 1/20 de miss.)",1,(255,255,255))
            choix_attaque3=font.render("2. Mega Coup de Poing (Entre 12 et 17 degats, 1/10 de miss.)",1,(255,255,255))
            choix_attaque4=font.render("3. Soin (Soigne entre 10 et 15 PV.)",1,(255,255,255))
            fen.blit(choix_attaque1, (150,430))
            fen.blit(choix_attaque2, (150,455))
            fen.blit(choix_attaque3, (150,490))
            fen.blit(choix_attaque4, (150,530))
            pygame.display.flip()

            player_move=0
            while player_move==0:
                for e in pygame.event.get():
                    if e.type == KEYDOWN:
                        if (e.key==K_1) or (e.key==K_KP1):
                            player_move="1"
                        if (e.key==K_2) or (e.key==K_KP2):
                            player_move="2"
                        if (e.key==K_3) or (e.key==K_KP3):
                            player_move="3"

            fen.blit(fond,(0,0))

            if player_move=="1":
                move_miss = random.randint(1,10) # 10% de chance de rater
                if move_miss == 1:
                    player_move = 0 # Le joueur rate et fait 0 dégats
                    atak=font.render("Vous avez rate !",1,(255,255,255))
                    fen.blit(atak, (150,30))
                    pygame.display.flip()
                else:
                    player_move = moves["Punch"]
                    atak=font.render("Vous donnez un coup de poing. Cela fait "+str(player_move)+" degats.",1,(255,255,255))
                    fen.blit(atak, (150,30))
                    pygame.display.flip()
            elif player_move=="2":
                move_miss = random.randint(1,5) # 20% de chance de rater
                if move_miss == 1:
                    player_move = 0 # Le joueur rate et fait 0 dégats
                    atak=font.render("Vous avez rate !",1,(255,255,255))
                    fen.blit(atak, (150,30))
                    pygame.display.flip()
                else:
                    player_move = moves["Mega Punch"]
                    atak=font.render("Vous donnez un mega coup de poing. Cela fait "+str(player_move)+" degats.",1,(255,255,255))
                    fen.blit(atak, (150,30))
                    pygame.display.flip()
            elif player_move=="3":
                heal_up = True # Soin activé
                player_move = moves["Heal"]
                atak=font.render("Vous vous soignez de "+str(player_move)+" points de vie.",1,(255,255,255))
                fen.blit(atak, (150,30))
                pygame.display.flip()

        else: # Tour de l'adversaire
            if enemy=="1" :
                move_miss = random.randint(1,7)
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:    
                    computer_move = 0 # L'adversaire rate et fait 0 dégats
                    atak=font.render("Votre adversaire a rate son attaque !",1,(255,255,255))
                    fen.blit(atak, (150,230))
                    pygame.display.flip()
                else:
                    computer_move = moves["Little Punch"]
                    atak1=font.render("Votre adversaire vous donne un petit coup de poing.",1,(255,255,255))
                    atak2=font.render(" Cela fait "+str(computer_move)+" degats.",1,(255,255,255))
                    fen.blit(atak1, (150,230))
                    fen.blit(atak2, (150,260))
                    pygame.display.flip()

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

        if player_turn:
            vie=font.render("Votre vie: "+str(player_health)+"   Vie de l'adversaire: "+str(computer_health), 1, (255,255,255))
            fen.blit(vie, (150,130))
            pygame.display.flip()
        else:
            vie=font.render("Votre vie: "+str(player_health)+"   Vie de l'adversaire: "+str(computer_health), 1, (255,255,255))
            fen.blit(vie, (150,330))
            pygame.display.flip()

        # Changement de tour
        player_turn = not player_turn
        computer_turn = not computer_turn