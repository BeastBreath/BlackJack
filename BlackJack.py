"""
This is a program for Black Jack
By: Nividh Singh
Date: 10/17/2022
"""

from codecs import getincrementaldecoder
import numbers
import random
from traceback import print_tb
import time

# Class for blackjack game
class BlackJack:
    # Lists to keep track of stuff as game goes on
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    cardNumbers = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    playerNames = []
    cards = []
    playerCards = []
    dealerCards = []
    playerBets = []
    playerMoney = []
    numberOfPlayers = 0

    # Finds player with the least score
    def minPlayer(self):
        minValue = self.value(self.playerCards[0])
        for i in range(self.numberOfPlayers):
            minValue = min(minValue, self.value(self.playerCards[i]))
        return minValue

    # Creates and shuffles a deck
    def makeDeck(self):
        self.cards.clear()
        for i in range(52):
            self.cards.append(i)
        random.shuffle(self.cards)

    # Deals the top card from the deck to the list given as a parameter
    def dealCard(self, cardsInHand):
        cardsInHand: list
        cardsInHand.append(self.getCard())

    # Gets card from the top of the pile
    def getCard(self):
        card = self.cards[0]
        self.cards = self.cards[1:]
        return card

    # Deals cards at the beginning of the game
    def deal(self):
        for i in range(self.numberOfPlayers):
            self.playerCards.append([self.getCard(), self.getCard()])
        self.dealerCards.append(self.getCard())

    # Prints player i's cards
    def printPlayerCards(self, i):
        i: int
        print(self.playerNames[i] + "\'s cards: ")
        for j in range(len(self.playerCards[i])):
            suit = self.suits[int(self.playerCards[i][j]/13)]
            cardNumber = self.cardNumbers[self.playerCards[i][j]%13]
            print("\t" + cardNumber + " of " + suit)

    # Prints dealers cards          
    def printDealersCards(self):
        print("Dealer's cards: ")
        for j in range(len(self.dealerCards)):
            suit = self.suits[int(self.dealerCards[j]/13)]
            cardNumber = self.cardNumbers[self.dealerCards[j]%13]
            print("\t" + cardNumber + " of " + suit)

    # Prints game instructions from file instructions
    def printInstructions(self):
        f = open("instructions.txt", "r")
        for line in f:
            print(line, end="")
        
    # Finds values of a list of cards
    def value(self, cardsInHand):
        cardsInHand: list
        value = 0
        aces = 0
        for card in range(len(cardsInHand)):
            cardValue = cardsInHand[card]%13 + 1
            
            # If ace add 11
            if cardValue == 1:
                value += 11
                aces += 1

            # If J, Q, or K add 10
            elif cardValue > 10:
                value += 10

            # Else add card value
            else:
                value += cardValue

        # While total is over 21, convert ace to 1
        while value > 21 and aces > 0:
            aces -= 1
            value -= 10
        return value
            
    # Plays a round of blackjack
    def playRound(self):

        # Goes through each player
        for player in range(self.numberOfPlayers):
            print(self.playerNames[player] + "\'s turn")
            bet = self.playerMoney[player] + 1
            print("You have: " + str(self.playerMoney[player]) + " dollars")

            # Gets bet from user
            while bet > self.playerMoney[player] and bet >= 0:
                bet = int(input("How much do you want to bet? "))
            self.playerBets.append(bet)

            #If player hits blackjack goes to next itteration of loop
            if self.value(self.playerCards[player]) == 21:
                print("You got a blackjack!")
                continue

            # Keeps going until player stands, doubles down or busts
            while True:
                self.printPlayerCards(player)

                command = input("> ")

                # If player chooses to hit
                if command.lower() == 'hit':
                    self.dealCard(self.playerCards[player])
                    if self.value(self.playerCards[player]) > 21:
                        print("BUST")
                        time.sleep(1)
                        self.printPlayerCards(player)
                        time.sleep(2)
                        break
                    elif self.value(self.playerCards[player]) == 21:
                        self.printPlayerCards(player)
                        break

                # If player chooses to stand
                elif command.lower() == 'stand':
                    break

                # If player chooses to double down
                elif command.lower() == 'double down':
                    if self.playerMoney[player] >= 2 * self.playerBets[player]:
                        self.playerBets[player] *= 2
                        self.dealCard(self.playerCards[player])
                        if self.value(self.playerCards[player]) > 21:
                            print("BUST")
                            time.sleep(1)
                        
                        self.printPlayerCards(player)
                        time.sleep(2)
                        break
                    else:
                        print("Not enough money to double down")

                else:
                    print("Invalid command")

        # Dealer plays to beat atleast one person
        self.printDealersCards()
        minToGet = self.minPlayer()
        while self.value(self.dealerCards) < minToGet or self.value(self.dealerCards) > 21:
            print("Dealer Hit")
            time.sleep(1)
            self.dealCard(self.dealerCards)
            self.printDealersCards()
            time.sleep(2)
        
        # Prints outcomes and changes player money totals
        for player in range(self.numberOfPlayers):

            # If player busts
            if self.value(self.playerCards[player]) > 21:
                print(self.playerNames[player] + " busted and lost his bet money")
                self.playerMoney[player] -= self.playerBets[player]

            # If the player beat the dealer
            elif self.value(self.playerCards[player]) > self.value(self.dealerCards) or (self.value(self.playerCards[player]) == self.value(self.dealerCards) and len(self.playerCards[player]) < len(self.dealerCards)):
                if self.value(self.playerCards[player]) == 21 and len(self.playerCards[player]) == 2:
                    print(self.playerNames[player] + " got a blackjack!")
                    self.playerMoney[player] += 1.5 * self.playerBets[player]
                else:
                    print(self.playerNames[player] + " beat the dealer!")
                    self.playerMoney[player] += self.playerBets[player]
            # If the player tied the dealer
            elif self.value(self.playerCards[player]) == self.value(self.dealerCards) and len(self.playerCards[player]) < len(self.dealerCards):
                print(self.playerNames[player] + " tied the dealer!")

            # If the player  dealer
            else:
                self.playerMoney[player] -= self.playerBets[player]
                print(self.playerNames[player] + " lost to the dealer!")

    # Resets game
    def reset(self):
        self.playerBets.clear()
        self.dealerCards.clear()
        self.playerCards.clear()
        self.makeDeck()
        self.deal()

    # Plays the game
    def playBlackJack(self):
        
        # Gets the number of players
        while 5 < self.numberOfPlayers or self.numberOfPlayers <= 0:
            self.numberOfPlayers = int(input("How many players are going to play (Max is 5)? "))
            
        # Gets names of players
        for player in range(self.numberOfPlayers):
            self.playerNames.append(input("What is player " + str(player + 1)+ "\'s name? "))

        # Sets up initial game
        self.playerMoney = [1000] * self.numberOfPlayers
        self.printInstructions()
        self.reset()

        # Keeps playing unitl players don't want to play again
        while True:
            self.playRound()
            self.reset()
            playAgain = input("Play again (y or n): ")
            if playAgain == 'n':
                break
        
        # Prints ending money totals
        for player in range(self.numberOfPlayers):
            print(self.playerNames[player] + " ended with " + str(self.playerMoney[player]) + " dollars")

# Creates instance of class and plays blackjack
bj = BlackJack()
bj.playBlackJack()