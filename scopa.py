import os
import random
import time
from enum import Enum

class Suit(Enum):
    CUPS = " of Cups"
    COINS = " of Coins"
    SWORDS = " of Swords"
    CLUBS = " of Clubs"

class Card:
    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit
    
    def __str__(self): 
        return "[" + str(self.value) + str(self.suit.value) + "]"

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

def getUserCommand(print_text: str):
    #prints prompt and returns user input converted to lowercase
    command = input(print_text + "\n")
    command = command.lower()
    return command

def printMenu():
    #starting menu sequence
    while 1:
        print("\n-----------------SCOPA-----------------")
        print("Welcome!")
        cmd = getUserCommand("What would you like to do? [ start | rules | quit ]")
        if cmd == "start":
            cmd = getUserCommand("How many players? [ one player | two player ]")
            if cmd == "one player" or cmd == "one" or cmd == '1':
                return False
            elif cmd == "two player" or cmd == "two" or cmd == '2':
                return True
            else:
                printBadInput()
        elif cmd == "rules":
            runHelpMenu()
        elif cmd == "quit":
            quit()
        else:
            printBadInput()
        os.system("cls")
    print("\n---------------------------------------\n")

def printRulesText():
    print("\n------------------RULES------------------")
    print("Scopa is an Italian game, so it is played with a 40-card deck with cards valuing from 1 to 10. The suits are Cups, Coins, Swords, and Clubs.")
    print("The goal of the game is to capture cards, so by the end of the game, scoring of your cards will grant you the most points.\n")

def printGameplayText():
    print("\n-----------------GAMEPLAY-----------------")
    print("Each player will be dealt 3 cards, and 4 face-up cards will be placed on the table.")
    print("You and the opponent will take turns playing one card each--either placing a card on the table or capturing cards.\n")
    print("Placing a card on the table removes it from your hand and adds it to the table. A card that can capture a card on the table cannot be played.\n")
    print("Capturing cards involves playing a card from your hand.")
    print("You can capture cards from the table if they add up to the value of a card in your hand.")
    print("This can be either with a single matching card, or a combination of several. After the card from your hand is played, both your card and the captured cards will be removed.\n")
    print("When both players run out of cards, then three cards are dealt to each.\n")
    print("If you clear the board during the round [exculding the last card played of the last round], that is called a SCOPA, which will add a point to your score.\n")
    
def printScoringText():
    print("\n-----------------SCORING-----------------")
    print("At the end of the game, all of the captured cards are evaluated.\n")
    print("Points can be gained for:")
    print("- Capturing the Seven of Coins")
    print("- Capturing the greatest number of cards")
    print("- Capturing the greatest number of Coin suited cards")
    print("- Having the highest \"Prime\".")
    print("---  A Prime is the total of adding the \"best\" card in each suit. The ranking is as follows:")
    print("---  [7]: 21pts. [6], 18pts. [1], 16pts. [5], 15pts. [4], 14pts. [3], 13pts. [2], 12 pts. [8/9/10], 10 pts.")
    print("\nKeep this in mind when capturing cards!")

def runHelpMenu():
    #displays rules & help 'screen'
    cmd = ""
    os.system('cls')
    printRulesText()
    print("[Press ENTER to proceed with GAMEPLAY rules or type \"EXIT\" to quit.]")
    cmd = getUserCommand(cmd)
    if (cmd == "exit"):
        return
    os.system('cls')
    printGameplayText()
    print("[Press ENTER to proceed with SCORING rules or type \"EXIT\" to quit.]")
    cmd = getUserCommand(cmd)
    if (cmd == "exit"):
        return
    while 1:
        os.system('cls')
        printScoringText()
        cmd = getUserCommand("\nWould you like to review anything? [ yes | no ]")
        if (cmd == "no" or cmd == "n"):
            return
        if (cmd == "yes" or cmd == "y"):
            cmd = getUserCommand("What would you like to review? [ rules | gameplay | scoring | exit ]")
            os.system('cls')
            while 1:
                if (cmd == "rules"):
                    printRulesText()
                elif (cmd == "gameplay"):
                    printGameplayText()
                elif (cmd == "scoring"):
                    printScoringText()
                elif (cmd == "exit"):
                    return
                cmd = getUserCommand("What would you like to review? [ rules | gameplay | scoring | exit ]")
                os.system('cls')
        else:
            printBadInput()

def initializeDeck():
    #creates and shuffles a deck of cards, returns deck
    pile = []
    for i in range(1, 11):
        pile.append(Card(i, Suit.CUPS))
        pile.append(Card(i, Suit.COINS))
        pile.append(Card(i, Suit.SWORDS))
        pile.append(Card(i, Suit.SWORDS))
    random.shuffle(pile)
    return pile

def findPrimeVal(num: int):
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
    printDealText()
    print("------The cards have been dealt.------\n")

def scoreCard(score, card):
    #compares given card to score's pertaining value and updates score if needed
    prime = 0
    score.numCards += 1
    prime = findPrimeVal(card.value)
    if (card.suit == Suit.CUPS):
        if score.cup_prime < prime:
            score.cup_prime = prime
    elif (card.suit == Suit.COINS):
        if card.value == 7:
            #the seven of coins
            score.sevenCoins += 1
        if score.coin_prime < prime:
            score.coin_prime = prime
    elif (card.suit == Suit.SWORDS):
        if score.sword_prime < prime:
            score.sword_prime = prime
    elif (card.suit == Suit.CLUBS):
        if score.club_prime < prime:
            score.club_prime = prime

def scoreDeck(score, p_hand):
    #scores entire hand of cards
    while (len(p_hand) > 0):
        scoreCard(score, p_hand.pop())

def printBadInput():
    #response to invalid input
    print("Please enter a valid command.")
    time.sleep(.7)

def printLines():
    #'animation' for dealing cards
    for i in range(0, 3):
        time.sleep(.175)
        print("/ ", end="", flush=True)

def printDealText():
    #complete text for dealing cards 'animation'
    os.system('cls')
    print("---------------------------------------\n")
    printLines()
    print("Dealing cards ", end="")
    printLines()
    time.sleep(.350)
    print("\n")
    os.system('cls')
    print("---------------------------------------\n")

def printComputerText():
    #'animation' for computer's turn
    printLines()
    print("Computer's turn ", end="")
    printLines()

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

def addScore(p1_field, p2_field, tally):
    #compares and adds a point to p1 or p2
    if p1_field > p2_field:
        tally[0] += 1
    elif p1_field < p2_field:
        tally[1] += 1

def addAllScores(p1_score, p2_score, tally):
    #compares and adds score up into tally
    addScore(p1_score.primeTotal, p2_score.primeTotal, tally)
    addScore(p1_score.numCoins, p2_score.numCoins, tally)
    addScore(p1_score.numCards, p2_score.numCards, tally)
    addScore(p1_score.sevenCoins, p2_score.sevenCoins, tally)
    tally[0] += p1_score.scopa
    tally[1] += p2_score.scopa

def scoring(p1_score, p2_score):
    #scoring sequence
    print("--SCORES--\n")
    print("PLAYER 1: ")
    printScore(p1_score)
    print("PLAYER 2: ")
    printScore(p2_score)
    tally = [0,0]
    addAllScores(p1_score, p2_score, tally)
    print("PLAYER 1 total: " + str(tally[0]))
    print("PLAYER 2 total: " + str(tally[1]) + "\n")
    if tally[0] > tally[1]:
        print("PLAYER 1 wins!")
    elif tally[1] > tally[0]:
        print("PLAYER 2 wins!")
    else:
        print("PLAYER 1 and PLAYER 2 are tied!")

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
                print("\n                            ", end="")
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

def printDeckSizeEstimate(deck):
    #takes in location int deck (int) and prints "visual" estimation of deck size
    if len(deck) <= 10:
        print("The deck has a few cards left.")
    elif len(deck) <= 25:
        print("The deck has about half of the cards left.")
    else:
        print("The deck has many cards left.")
    time.sleep(.7)

def checkPlayable(total: int, table: list[Card], matches: list[Card]):
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

def validateHandIndexChoice(place, hand):
    #checks if user's selected index (location on table) is valid
    try:
        place = int(place)
    except ValueError:
        printBadInput()
        return False
    if place > 0 and place <= len(hand):
        return True
    else:
        printBadInput()
        return False

def playerPlaceCard(p_hand: list[Card], table: list[Card]):
    #player inputs card from hand, card is added to table if no other moves
    place = getUserCommand("Which card? Type the position in hand (i.e. 1, 2, 3).")
    if validateHandIndexChoice(place, p_hand):
        #card/index can be played
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

def processList(nums: list):
    #converts list of strings to int
    for i in range(len(nums)):
        try:
            nums[i] = int(nums[i]) - 1
        except ValueError:
            return False
    return True

def checkValidCapture(target: int, nums: list[int], table: list[Card], cards: list[Card]):
    #verifies that list adds up to chosen value
    total = 0
    for x in nums:
        try:
            c = table[x]
            total += c.value
            if c in cards:
                return False
            cards.append(c)
        except:
            return False
    if total == target:
        return True
    return False
    
def playerCaptureCard(p_score: Score, p_hand: list[Card], table: list[Card]):
    #player inputs card from hand and card(s) from table they want to capture. cards are removed and scored.
    # returns true on a successful/valid capture (returns false if a player selects an invalid set of cards, etc)

    # cannot capture cards if there are no cards on the table
    if len(table) == 0:
        print("There are no cards to capture.")
        time.sleep(.35)
    else:
        place = getUserCommand("Which card from your hand do you want to play? Type position in hand (i.e. 1, 2, 3).")
        if validateHandIndexChoice(place, p_hand):
            #card can be played
            selectedCard = p_hand[int(place) - 1]

            # display cards WITH INDEXES on the table for selection:
            #   -1- [7 of Swords]
            #   -2- [9 of Swords]
            #   ...etc
            os.system("cls") # clear the screen
            print("\n---------------------------------------")
            print("Your card: " + str(selectedCard) + "\n")
            for index, x in enumerate(table):
                print("-" + str(index + 1) + "- " + str(x))
            cmd = getUserCommand("\nWhich cards on the table? Type position on table separated by a space (e.g. 3 1 5).")
            nums = cmd.split() # split between spaces
            selectedCards = []
            # make sure all inputs are integers, and the capture is valid (table cards sum to equal played card)
            if processList(nums) and checkValidCapture(selectedCard.value, nums, table, selectedCards):
                for x in selectedCards:
                    # when a card is captured, it is removed from the table and added to the player's score & posession
                    table.remove(x)
                    scoreCard(p_score, x)
                # when a card is played, it is removed from the player's hand and added to the player's score & posession
                p_hand.remove(selectedCard)
                scoreCard(p_score, selectedCard)
                
                # check for scopa
                if (len(table) == 0):
                    os.system("cls")
                    print("\n\n----SCOPA!----")
                    # record the scopa in the player's score
                    p_score.scopa += 1
                    time.sleep(.7)
                return True
            else:
                printBadInput()
                return False

def userAction(p_score: Score, p_hand: list[Card], op_hand: list[Card], table: list[Card], turn1, deck):
    #the player's turn: displays options and carries out specified action
    while 1:
        #print the cards to the screen
        displayCards(p_hand, op_hand, table, turn1)
        #if a player has no cards left, they skip their turn and end their action
        if len(p_hand) == 0:
            print("You have no more cards.")
            time.sleep(.7)
            return
        #the player has cards in their hand, so ask what they would like to do
        cmd = getUserCommand("What would you like to do? [ capture card | place card | sort cards | check deck | help ]")
        # parse the input, run the appropriate command/menu
        if (cmd == "capture card"):
            if playerCaptureCard(p_score, p_hand, table):
                # return because the action/turn is complete on a successful capture
                return
        elif (cmd == "place card"):
            if playerPlaceCard(p_hand, table):
                # return because the action/turn is complete on a successful placement
                return
        elif (cmd == "sort cards" or cmd == "sort"):
            p_hand.sort(key=lambda x: x.value, reverse=True)
            # sort cards, continue this loop because the action/turn isn't over
        elif (cmd == "check deck"):
            printDeckSizeEstimate(deck)
            # print deck size, continue this loop because the action/turn isn't over
        elif (cmd == "help"):
            runHelpMenu()
            # run help menu, continue this loop because the action/turn isn't over
        elif cmd == "quit" or cmd == "exit":
            cmd = getUserCommand("Are you sure you would like to quit the game? [ yes | no ]")
            # quit the game immediately
            if cmd == "y" or cmd == "yes":
                quit()
        else:
            # couldn't parse the user's input, continue this action/turn
            printBadInput()

def computerAction(c_score: Score, c_hand: list[Card], table: list[Card]):
    #code goes here

    # demo code
    # check that there are cards in hand and table
    if len(c_hand) > 0 and len(table) > 0:
        firstHandCard = c_hand[0]
        firstTableCard = table[0]
        # take the first card in the hand and the first card on the table if:
        # 1. they match in value
        # 2. the table card is a Coins card
        if firstTableCard.suit == Suit.COINS and firstHandCard.value == firstTableCard.value:
            table.remove(firstHandCard)
            scoreCard(c_score, firstHandCard)
            
    
def main():
    two_player = printMenu()
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
    while (1):
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
                break
        if turn1:
            print("\n----PLAYER 1----")
            playerBuffer()
            userAction(p1_score, p1_hand, p2_hand, table, turn1, deck)
        else:
            if two_player:
                print("\n----PLAYER 2----")
                playerBuffer()
                userAction(p2_score, p2_hand, p1_hand, table, turn1, deck)
            else:
                printComputerText()
                computerAction(p2_score, p2_hand, table) #create this function
        turn1 = not turn1
        os.system("cls")
        print("---------------------------------------\n")
    
    #end of game
    os.system("cls")
    print("---------------------------------------\n")
    scoring(p1_score, p2_score)
    time.sleep(.35)
    buffer("\nPress ENTER to exit.")
    

if __name__ == "__main__":
    main()