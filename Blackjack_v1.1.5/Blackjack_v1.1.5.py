import random
import time
import os
from colorama import init, Fore

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # def __str__(self):
    #     return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    # def __str__(self):
    #     deck_comp = '=== The Deck ==='
    #     for card in self.deck:
    #         deck_comp += '\n' + card.__str__()
    #     return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self, card):
        self.cards.append(card)
        if card.rank == 'Ace':
            self.aces += 1
        if self.aces == 2:
            self.value = input("Do you want to start with '2' or '12': ")
            self.aces = 0
            pass
        self.value += values[card.rank]
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Slot:
    def __init__(self, chips = 100, played = 0):
        self.chips = chips
        self.played = played

    def __del__(self):
        pass

def title():
    print('♠ ♥ ♦ ♣ WELCOME TO BLACKJACK ♣ ♦ ♥ ♠\n')

def take_bet():
    global bet
    while True:
        try:
            bet = int(input('How many chips would you like to bet: '))
        except ValueError:
            print('Sorry, please provide an integer.')
        else:
            if bet <= 0:
                print('Sorry, please bet at least 1 chips.')
            elif bet > chips:
                print(f"Sorry, you don't have enough chips! You have: {chips}")
            else:
                break

def win_bet():
    global chips
    chips += bet

def lose_bet():
    global chips
    chips -= bet
    if chips < 0:
        chips = 0

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop
    while True:
        choice = input("Hit or Stand? Enter 'H' or 'S': ")
        try:
            if choice[0].upper() == 'H':
                clear()
                print('Player HITS!!!')
                hit(deck, hand)
                if player_hand.value == 21:
                    show_some(player_hand, dealer_hand)
                    time.sleep(3)
                    clear()
                else:
                    show_some(player_hand, dealer_hand)
            elif choice[0].upper() == 'S':
                clear()
                print("Player Stands, Dealer's Turn.")
                time.sleep(1)
                playing = False
            else:
                print("Sorry, please enter 'H' or 'S'.")
                continue
        except:
            print('Sorry, please enter something.')
            continue
        break

def show_some(player_hand, dealer_hand):
    """Show only one of the Dealer's cards, the other remains hidden."""
    print("=== Dealer's Cards ===")
    print(ascii_version_of_hidden_card(*dealer_hand.cards))
    print("=== Player's Cards ===")
    print(ascii_version_of_card(*player_hand.cards))
    print('')
    
def show_all(player_hand, dealer_hand):
    print("=== Dealer's Cards ===")
    print(ascii_version_of_card(*dealer_hand.cards))
    print("=== Player's Cards ===")
    print(ascii_version_of_card(*player_hand.cards))
    print('')

def blackjack_win():
    print('BLACKJACK!!!')
    global chips
    chips += bet * 0.5

def player_busts():
    print('PLAYER BUSTED!!! DEALER WINS!!!')
    lose_bet()

def player_wins():
    print('PLAYER WINS!!!')
    win_bet()

def dealer_busts():
    print('PLAYER WINS!!! DEALER BUSTED!!!')
    win_bet()
    
def dealer_wins():
    print('DEALER WINS!!!')
    lose_bet()
    
def push():
    print('PLAYER and DEALER TIE, PUSH!!!')

def replay():
    """Ask the player if they want to play again."""
    while True:
        play = input('Would you like to play another hand? [Y/n]: ')
        try:
            if play.upper() == 'Y':
                return True
            elif play.lower() == 'n':
                return False
            else:
                print("Sorry, please enter 'Y' or 'n'.")
                continue
        except:
            print('Sorry, please enter something.')
        else:
            break

def ascii_version_of_card(*cards, return_string = True):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    # we will use this to prints the appropriate icons for each card
    suits_symbols = {'Clubs':'♣', 'Diamonds':'♦', 'Hearts':'♥', 'Spades':'♠'}

    # create an empty list of list, each sublist is a line
    lines = [[] for _ in range(9)]

    for card in cards:
        # "King" should be "K" and "10" should still be "10"
        if card.rank == '10':  # ten is the only one who's rank is 2 char long
            rank = card.rank
            space = ''  # if we write "10" on the card that line will be 1 char too long
        else:
            rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to fill the void
        # get the cards suit in two steps
        suit = suits_symbols[card.suit]

        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = (''.join(line) for line in lines)

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result

def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    # a flipper over card. # This is a list of lists instead of a list of string becuase appending to a list is better than adding a string
    lines = ['┌─────────┐'] + ['│░░░░░░░░░│']*7 + ['└─────────┘']

    # store the non-flipped over card after the one that is flipped over
    cards_except_first = ascii_version_of_card(*cards[1:], return_string = False)
    # for index, line in enumerate(cards_except_first):
    #     lines[index].append(line)

    # make each line into a single list
    # for index, line in enumerate(lines):
    #     lines[index] = ''.join(line)

    # # convert the list into a single string
    # return '\n'.join(lines)
    return '\n'.join([x + y for x, y in zip(lines, cards_except_first)])

def load():
    to_menu = True # use for return to menu
    while to_menu:
        to_menu = False
        clear()
        title() # display title 
        # time.sleep(1)
        print('=== SELECT OPTIONS ===')
        print('❶ New Game')
        print('❷ Load Game')
        print('❸ Quit')
        global ready, chips, played, slot
        nums = ('❶', '❷', '❸', '❹', '❺')
        slots = []
        while True and not to_menu: # input option
            try:
                option = int(input('>>> Option: '))
            except ValueError:
                print('Sorry, please enter the following options number.')
                continue
            else:
                ready = True
                if option == 1: # new game
                    try:
                        with open('database.txt', 'x+') as f: # no file exist
                            f.write('Empty\n'*5)
                    except FileExistsError: # file exist
                        with open('database.txt', 'r') as f: # read exist file
                            lines = f.read().splitlines()
                            for line in lines:
                                slots.append(line.split(','))
                    else:
                        with open('database.txt', 'r') as f:
                            lines = f.read().splitlines()
                            for line in lines:
                                slots.append(line.split(','))
                    clear()
                    title() # display title 
                    print('=== SELECT YOUR SAVE SLOT ===')
                    for i in range(5):
                        print(f'< Slot {nums[i]} >')
                        if slots[i][0] == 'Empty':
                            print('\tEmpty Slot')
                        else:
                            print(f'\tChip(s): {slots[i][0]}\n\tTime(s) Played: {slots[i][1]}')
                    while True:
                        try:
                            slot = int(input('>>> Slot[Press 0 to Menu]: '))
                        except ValueError:
                            print('Sorry, please enter the slot number.')
                            continue
                        else:
                            if slot == 0:
                                to_menu = True
                            else:
                            # elif slots[slot][0] != 'Empty':
                            #     while True:
                            #         try:
                            #             override = input('Do you want to override your data? [Y/n]: ')
                            #         except:
                            #             print('Sorry, please enter something.')
                            #             continue
                            #         else:
                            #             if override.upper() == 'Y':
                            #                 break 
                            #             elif override.lower() == 'n':
                            #                 to_menu = True
                            #                 break
                                save(slot, new = True)
                                break
                elif option == 2: # load game
                    try:
                        with open('database.txt', 'r') as f: # read exist file
                            lines = f.read().splitlines()
                            for line in lines:
                                slots.append(line.split(','))
                    except FileNotFoundError: # no exist file
                        with open('database.txt', 'x+') as f:
                            f.write('Empty\n'*5)
                        with open('database.txt', 'r') as f:
                            lines = f.read().splitlines()
                            for line in lines:
                                slots.append(line.split(','))
                    clear()
                    title() # display title 
                    print('=== SELECT YOUR SAVE SLOT ===')
                    for i in range(5):
                        print(f'< Slot {nums[i]} >')
                        if slots[i][0] == 'Empty':
                            print('\tEmpty Slot')
                        else:
                            print(f'\tChip(s): {slots[i][0]}\n\tTime(s) Played: {slots[i][1]}')
                    while True:
                        try:
                            slot = int(input('>>> Slot[Press 0 to Menu]: '))
                        except ValueError:
                            print('Sorry, please enter the slot number.')
                            continue
                        else:
                            if slot == 0:
                                to_menu = True
                                break
                            elif slots[slot-1][0] == 'Empty':
                                print('Sorry, that slot is empty.')
                                continue
                            else:
                                chips = float(slots[slot-1][0])
                                played = float(slots[slot-1][1])
                                break
                elif option == 3: # quit
                    print('The Player Has Quit.')
                    ready = False
                else:
                    print('Sorry, please enter the following options number.')
                    continue
                break
    
def save(slot, new = False):
    global chips, played
    with open('database.txt', 'r') as f: # read exist file
        lines = f.readlines()
    if new:
        chips = 100.0
        played = 0
    lines[slot-1] = f'{chips},{played}\n' # replace
    with open('database.txt', 'w') as out:
        out.writelines(lines) # rewrite

def delete(slot):
    pass

if __name__ == '__main__':
    # Setup
    suits = ('Clubs','Diamonds', 'Hearts', 'Spades' )
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

    clear = lambda : os.system('cls')
    init(autoreset = True)

    # Preparation
    chips = 100 # default
    played = 0 # default
    broke = False # default

    load() # load game
    while ready:
        clear()
        # print('『 GAME START 』\n')
        # print('<< GAME START >>\n')
        playing = True
        blackjack = False
        deck = Deck() # create a new Deck Object
        deck.shuffle() # shuffle the Deck

        dealer_hand = Hand() # create new Dealer's Hand Object
        player_hand = Hand() # create new Player's Hand Object

        take_bet() # ask the Player for their bet

        dealer_hand.add_card(deck.deal()) # deal two cards to the Dealer
        dealer_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal()) # deal two cards to the Player
        player_hand.add_card(deck.deal())

        show_some(player_hand, dealer_hand) # display cards
        if player_hand.value == 21: # check Blackjack
            time.sleep(2)
            clear()
            blackjack = True
        while playing:
            busted = False
            if player_hand.value < 21:
                hit_or_stand(deck, player_hand) # prompting the Player to Hit or Stand
                continue
            # Player Busted
            elif player_hand.value > 21:
                player_busts()
                busted = True
            break
        if not busted:
            if dealer_hand.value >= 17:
                print('Dealer Stand.')
            while dealer_hand.value < 17: # S17
                hit(deck, dealer_hand)
                print('Dealer HITS!!!')
            show_all(player_hand, dealer_hand) # display all cards
            # Player Wins
            if player_hand.value > dealer_hand.value:
                if blackjack:
                    blackjack_win()
                player_wins()
            # Dealer Busted
            elif dealer_hand.value > 21:
                if blackjack:
                    blackjack_win()
                dealer_busts()
            # Dealer Wins
            elif player_hand.value < dealer_hand.value:
                dealer_wins()
            # Push
            elif player_hand.value == dealer_hand.value:
                push()

        played += 1 # add played times
        # Inform Player of their chips total
        time.sleep(3)
        print(f'Player total chips: {chips}\n')
        if chips == 0:
            time.sleep(3)
            print('GAME OVER!!! YOU ARE BROKE!!!')
            chips = 'Broke'
            broke = True
        save(slot) # save game
        # Play again?
        time.sleep(3)
        if broke:
            print('THANK YOU FOR PLAYING!!!')
            time.sleep(3)
            break
        elif not replay():
            print('THANK YOU FOR PLAYING!!!')
            time.sleep(3)
            break
        else:
            playing = True
            clear()