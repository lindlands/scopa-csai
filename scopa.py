import os
import random
import time
import sys

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self): 
        return "[" + str(self.value) + self.suit + "]"

class Score(object):
    def __init__(self):
        self.numCards = 0
        self.sevenCoins = 0
        self.numCoins = 0
        self.primeTotal = 0
        self.scopa = 0
        self.cup_prime = 0
        self.coin_prime = 0
        self.sword_prime = 0
        self.club_prime = 0

def getCommand(print_text):
    #prints prompt and returns user input converted to lowercase
    command = input(print_text + "\n")
    command = command.lower()
    return command

def rulesText():
    print("\n------------------RULES------------------")
    print("Scopa is an Italian game, so it is played with a 40-card deck with cards valuing from 1 to 10. The suits are Cups, Coins, Swords, and Clubs.")
    print("The goal of the game is to collect cards, so by the end of the game, scoring of your cards will grant you the most points.\n")

def gameplayText():
    print("\n-----------------GAMEPLAY-----------------")
    print("Each player will receive 3 cards, and there are 4 face-up cards played on the table.")
    print("You and the opponent will take turns either placing a card on the table or capturing cards.\n")
    print("Placing a card on the table removes it from your hand and adds it to the table. A card that can capture a card on the table cannot be played.\n")
    print("Capturing cards involves playing a card from your hand.")
    print("You can capture cards from the table if they add up to the value of a card in your hand. This can be either with a single matching card, or a combination of several. After the card from your hand is played, both your card and the captured cards will be removed.\n")
    print("When both players run out of cards, then three cards are dealt to each.\n")
    print("If you clear the board during the round [exculding the last card played of the last round], that is called a SCOPA, which will add a point to your score.\n")
    
def scoringText():
    print("\n-----------------SCORING-----------------")
    print("At the end of the game, all of the captured cards are evaluated.\n")
    print("Points can be gained for:")
    print("- Capturing the Seven of Coins")
    print("- Capturing the greatest number of cards")
    print("- Capturing the greatest number of Coins")
    print("- Having the highest \"Prime\".")
    print("---  A Prime is the total of adding the \"best\" card in each suit. The ranking is as follows:")
    print("---  [7]: 21pts. [6], 18pts. [1], 16pts. [5], 15pts. [4], 14pts. [3], 13pts. [2], 12 pts. [8/9/10], 10 pts.")
    print("\nKeep this in mind when capturing cards!")

def helpText():
    #displays rules 'screen'
    cmd = ""
    os.system('cls')
    rulesText()
    print("[Press ENTER to proceed with GAMEPLAY rules or type \"EXIT\" to start playing.]")
    cmd = getCommand(cmd);
    if (cmd == "exit"):
        return
    os.system('cls')
    gameplayText()
    print("[Press ENTER to proceed with SCORING rules or type \"EXIT\" to start playing.]")
    cmd = getCommand(cmd);
    if (cmd == "exit"):
        return;
    while 1:
        os.system('cls')
        scoringText()
        cmd = getCommand("\nAre you ready to play? [yes/no]")
        if (cmd == "yes" or cmd == "y"):
            return
        if (cmd == "no" or cmd == "n"):
            cmd = getCommand("What would you like to review? [rules/gameplay/scoring/exit]")
            os.system('cls')
            while 1:
                if (cmd == "rules"):
                    rulesText()
                elif (cmd == "gameplay"):
                    gameplayText()
                elif (cmd == "scoring"):
                    scoringText()
                elif (cmd == "exit"):
                    return
                cmd = getCommand("What would you like to review? [rules/gameplay/scoring/exit]")
                os.system('cls')

def initializeDeck():
    #creates and shuffles a deck of cards, returns deck
    pile = []
    for i in range(1, 11):
        pile.append(Card(i, " of Cups"))
        pile.append(Card(i, " of Coins"))
        pile.append(Card(i, " of Swords"))
        pile.append(Card(i, " of Clubs"))
    random.shuffle(pile)
    return pile

def findPrimeVal(num):
    #calculates the prime value of one number
    if num == 7:
        return 21
    elif num == 6:
        return 18
    elif num == 1:
        return 16
    elif num == 5:
        return 15
    elif num == 4:
        return 14
    elif num  == 3:
        return 13
    elif num == 2:
        return 12
    else:
        #face cards
        return 10

def dealCards(deck, p1_hand, p2_hand):
    #adds three cards from the deck to players' hands
    for i in range(0, 3):
        if len(deck) <= 1:
            break
        p1_hand.append(deck.pop())
        p2_hand.append(deck.pop())

def scoreCard(score, card):
    #compares given card to score's pertaining value and updates score if needed
    prime = 0
    score.numCards += 1
    prime = findPrimeVal(card.value)
    if (card.suit == " of Cups"):
        if score.cup_prime < prime:
            score.cup_prime = prime
    elif (card.suit == " of Coins"):
        if card.value == 7:
            #the seven of coins
            score.sevenCoins += 1
        if score.coin_prime < prime:
            score.coin_prime = prime
    elif (card.suit == " of Swords"):
        if score.sword_prime < prime:
            score.sword_prime = prime
    elif (card.suit == " of Clubs"):
        if score.club_prime < prime:
            score.club_prime = prime

def scoreDeck(score, p_hand):
    #scores entire hand of cards
    while (len(p_hand > 0)):
        scoreCard(score, p_hand.pop)

def dealingText():
    #'animation' for dealing cards
    for i in range(0, 3):
        time.sleep(.175)
        print("/ ", end="", flush=True)

def dealText():
    #complete text for dealing cards 'animation'
    os.system('cls')
    print("---------------------------------------\n")
    dealingText()
    print("Dealing cards ", end="")
    dealingText()
    time.sleep(.350)
    print("\n")
    os.system('cls')
    print("---------------------------------------\n")

def buffer(text):
    #waits for \n to continue
    print(text)
    cmd = 'a'
    while cmd !='':
        cmd = input()
    os.system('cls')
    print("---------------------------------------\n")
    
def playerBuffer():
    #displays 'screen' that waits for \n to continue
    buffer("Press ENTER to start turn.")

def printCards(hand):
    #prints all cards in given list
    place = 0
    if (len(hand) == 0):
        print("There are no cards.")
    else:
        for x in hand:
            print(x, end="")
            if place != len(hand) - 1:
                #don't print comma on last card
                print(", ", end="")
            if (place % 3 == 0 and place != 0 and place != len(hand) - 1):
                #formatting
                print("\n                            ", end="");
            place += 1
        print("")

def displayCards(p_hand, op_hand, table, turn1):
    #prints cards of player and table, and the number of cards of the opponent.
    os.system("cls")
    print("\n---------------------------------------")
    if (turn1):
        print("----PLAYER 1----")
    else:
        print("----PLAYER 2----")
    print("The cards in your hand are: ",end="")
    printCards(p_hand)
    print("The cards on the table are: ",end="")
    printCards(table)
    print("Your opponent has ",end="")
    if len(op_hand) == 1:
        print("1 card.\n")
    else:
        print(str(len(op_hand)) + " cards.\n")

def checkPlayable(total, table, matches):
    #recursively finds all combinations of table's cards that add to total
    matches_size = len(matches)
    for focus in table:
        if total - focus.value == 0:
            matches.append(focus)
        elif total - focus.value > 0:
            checkPlayable(total - focus.value, table[table.index(focus) + 1:], matches)
            if (len(matches) > matches_size):
                matches.append(focus)
                matches_size = len(matches)

def badInput():
    #response to invalid input
    print("Please enter a valid command.")
    time.sleep(.7)

def plausibleCard(place, hand):
    #checks if card can be played
    try:
        place = int(place)
    except ValueError:
        badInput()
        return False
    if place > 0 and place <= len(hand):
        return True
    else:
        badInput()
        return False

def checkCards(target, nums, table, cards):
    #verifies that list adds up to chosen value
    total = 0
    for x in nums:
        try:
            c = table[int(x) - 1]
            total += c.value
            if c in cards:
                return False
            cards.append(c)
        except:
            return False
    if total == target:
        return True
    return False

def deckSize(deck):
    #takes in location int deck (int) and prints "visual" estimation of deck size
    if len(deck) <= 10:
        print("The deck has a few cards left.")
    elif len(deck) <= 25:
        print("The deck has about half of the cards left.")
    else:
        print("The deck has many cards left.")
    time.sleep(.7)

def captureCard(p_score, p_hand, table):
    #player inputs card from hand and card(s) from table they want to capture. cards are removed and scored.
    if len(table) == 0:
        print("There are no cards to capture.")
        time.sleep(.35)
    else:
        place = getCommand("Which card from your hand do you want to play? Type position in hand (i.e. 1, 2, 3).")
        if plausibleCard(place, p_hand):
            #card can be played
            c = p_hand[int(place) - 1]
            os.system("cls")
            print("\n---------------------------------------")
            print("Your card: " + str(c) + "\n")
            for index, x in enumerate(table):
                print("-" + str(index + 1) + "- " + str(x))
            cmd = getCommand("\nWhich cards on the table? Type position on table separated by a space (e.g. 3 1 5).")
            nums = cmd.split()
            inputCards = []
            if checkCards(c.value, nums, table, inputCards):
                for x in inputCards:
                    table.remove(x)
                    scoreCard(p_score, x)
                p_hand.remove(c)
                scoreCard(p_score, c)
                if (len(table) == 0):
                    os.system("cls")
                    print("\n\n----SCOPA!----")
                    p_score.scopa += 1
                    time.sleep(.7)
                return True
            else:
                badInput()
                return False
    
def placeCard(p_hand, table):
    #player inputs card from hand, card is added to table if no other moves
    place = getCommand("Which card? Type the position in hand (i.e. 1, 2, 3).")
    if plausibleCard(place, p_hand):
        #card can be played
        c = p_hand[int(place) - 1]
        pos = []
        checkPlayable(c.value, table, pos)
        if len(pos) != 0:
            print("A card can only be placed on the table when there are no cards to capture.")
            time.sleep(.7)
            return False
        else:
            table.append(p_hand.pop(int(place) - 1))
            return True

def action(p_score, p_hand, op_hand, table, turn1, deck):
    #the player's turn: displays options and carries out specified action
    while 1:
        displayCards(p_hand, op_hand, table, turn1)
        if len(p_hand) == 0:
            print("You have no more cards.")
            time.sleep(.7)
            return
        cmd = getCommand("What would you like to do? [ capture card | place card | sort cards | check deck | help ]")
        if (cmd == "capture card"):
            if captureCard(p_score, p_hand, table):
                return
        elif (cmd == "place card"):
            if placeCard(p_hand, table):
                return
        elif (cmd == "sort cards" or cmd == "sort"):
            p_hand.sort(key=lambda x: x.value, reverse=True)
        elif (cmd == "check deck"):
            deckSize(deck)
        elif (cmd == "help"):
            helpText()
        else:
            badInput()

def printScore(p_score):
    #prints the player's score

    print("Number of cards captured: " + str(p_score.numCards))
    time.sleep(.35)
    print("Number of Coins captured: " + str(p_score.numCoins))
    time.sleep(.35)
    print("Number of Scopas: " + str(p_score.scopa))
    time.sleep(.35)
    #add up primes
    p_score.primeTotal += p_score.club_prime
    p_score.primeTotal += p_score.coin_prime
    p_score.primeTotal += p_score.cup_prime
    p_score.primeTotal += p_score.sword_prime
    print("Prime: " + str(p_score.primeTotal))
    time.sleep(.35)
    if p_score.sevenCoins == 1:
        print("You captured the 7 of Coins.")
    time.sleep(.7)
    print("\n")

def addScore(p1_field, p2_field, p1, p2):
    #compares and adds a point to p1 or p2
    if p1_field > p2_field:
        p1+=1
    elif p1_field > p2_field:
        p2+=1

def addAllScores(p1_score, p2_score, p1, p2):
    #compares and adds score up into p1/p2
    addScore(p1_score.primeTotal, p2_score.primeTotal, p1, p2)
    addScore(p1_score.numCoins, p2_score.numCoins, p1, p2)
    addScore(p1_score.numCards, p2_score.numCards, p1, p2)
    addScore(p1_score.sevenCoins, p2_score.sevenCoins, p1, p2)
    p1 += p1_score.scopa
    p2 += p2_score.scopa

def scoring(p1_score, p2_score):
    #scoring sequence
    print("--SCORES--\n")
    print("PLAYER 1: ")
    printScore(p1_score)
    print("PLAYER 2: ")
    printScore(p1_score)
    p1 = 0
    p2 = 0
    addAllScores(p1_score, p2_score, p1, p2)
    print("PLAYER 1 total: " + str(p1))
    print("PLAYER 2 total: " + str(p2) + "\n")
    if p1 > p2:
        print("PLAYER 1 wins!")
    elif p2 > p1:
        print("PLAYER 2 wins!")
    else:
        print("PLAYER 1 and PLAYER 2 are tied!")
    
    
def main():
    print("\n-----------------SCOPA-----------------")
    print("Welcome!")
    while 1:
        cmd = getCommand("Do you know how to play scopa?")
        if (cmd == "yes"):
            break
        if (cmd == "no"):
            helpText()
            print("Okay, we'll get right into it. Good luck! \n")
            break
        else:
            print("Please enter either yes or no.")
            os.system('cls')
        os.system('cls')
    print("\n---------------------------------------\n")

    deck = []
    table = []
    p1_hand = []
    p2_hand = []
    p1_score = Score()
    p2_score = Score()
    turn1 = True
    deck = initializeDeck()
    for i in range(0, 4):
        #deals cards to the table
        table.append(deck.pop())
    state = 0
    while (state == 0):
        #main part of the game
        if len(p1_hand) == 0 and len(p2_hand) == 0:
            dealCards(deck, p1_hand, p2_hand)
            if len(p1_hand) == 0 and len(p2_hand) == 0:
                #no more cards left
                if turn1:
                    #remaining cards go to p2
                    scoreDeck(p2_score, table)
                else:
                    #remaining cards go to p1
                    scoreDeck(p1_score, table)
                state = 1
            dealText()
            print("------The cards have been dealt.------\n")
        if turn1:
            print("\n----PLAYER 1----")
            playerBuffer()
            action(p1_score, p1_hand, p2_hand, table, turn1, deck)
        else:
            print("\n----PLAYER 2----")
            playerBuffer()
            action(p2_score, p2_hand, p1_hand, table, turn1, deck)
        turn1 = not turn1
        os.system("cls")
        print("---------------------------------------\n")
    
    #end of game
    scoring()
    time.sleep(.35)
    buffer("\nPress ENTER to exit.")
    

if __name__ == "__main__":
    main()