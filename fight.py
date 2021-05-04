import random


def main():
    play_again = True

    while play_again:
        winner = None
        player_health = 100
        computer_health = 100

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
            miss = False # Détermine si l'attaque choisie va rater.

            # Crée un dictionnaire des mouvements possibles et choisi aléatoirement les dégats/soins effectués.
            moves = {"Punch": random.randint(18, 25),
                     "Mega Punch": random.randint(10, 35),
                     "Heal": random.randint(20, 25)}

            if player_turn:
                print("\nSelectionnez une attaque:\n1. Coup de Poing (Faire entre 18 à 25 points de dégats)\n2. Méga Coup de Poing (Faire entre 10 à 5 points de dégats)\n3. Soin (Soigne entre 20 et 25 points de vie)\n")

                player_move = input("> ").lower()

                move_miss = random.randint(1,10) # 10% de chance de rater
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:
                    player_move = 0 # Le joueur rate et fait 0 dégats
                    print("Vous avez raté !")
                else:
                    if player_move in ("1", "poing","coup de poing"):
                        player_move = moves["Punch"]
                        print("\nVous donnez un coup de poing. Cela fait ", player_move, " dégâts.")
                    elif player_move in ("2", "mega poing","mega coup de poing"):
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

                move_miss = random.randint(1,5)
                if move_miss == 1:
                    miss = True
                else:
                    miss = False

                if miss:
                    computer_move = 0 # L'adversaire rate et fait 0 dégats
                    print("Votre adversaire a raté son attaque !")
                else:
                    computer_move = moves["Punch"]
                    print("\nVotre adversaire vous donne un coup de poing. Cela fait ", computer_move, " dégats.")

            if heal_up:
                player_health += player_move
                if player_health > 100:
                    player_health = 100 # PV maximum de 100!
            else:
                if player_turn:
                    computer_health -= player_move
                    if computer_health < 0:
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

        play_again = False

main()