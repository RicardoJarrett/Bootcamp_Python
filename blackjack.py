import pygame
import random
import time
from enum import Enum
import os
"""
Using pygame for window, rendering, input
using random for deck shuffling, time to seed random
using os for path
"""

"""
I didn't expect such a large project. I should have split this into modules.
plan to move globals into a dedicated module.
gather rendering, objects, helper funcs
"""

pygame.init()
font = pygame.font.SysFont('arial', 15)
text = ""
text_texture = font.render(text, True, (0,0,0))
money_text_texture = font.render("Money: 100", True, (0,0,0))
bet_text_texture = font.render("Bet: 10", True, (0,0,0))

def update_money_text():
    global money_text_texture
    global bet_text_texture
    
    money_text_texture = font.render("Money: " + str(player.money), True, (0,0,0))
    bet_text_texture = font.render("Bet: " + str(player.current_bet), True, (0,0,0))
    return

def cPrint(in_text):
    global text
    global text_texture
    text += " " + in_text
    text_texture = font.render(text, True, (0,0,0))
    return

def cPrintClear():
    global text
    global text_texture
    text = ""
    text_texture = font.render("", True, (0,0,0))
    return

"""
Path to card images.
os.path.join  joins   os.path.dirname(__file__)   and   card_path
os.path.dirname(__file__)   is used to find where this file (blackjack.py) is located, and to find paths relative to this.
"""

#image loading has been spread out, to show its composition
current_file_path = os.path.dirname(__file__)
card_path = "blackjack\\playing_cards\\cards_scaled.png"
loadable_card_path = os.path.join(current_file_path, card_path)
card_spritesheet = pygame.image.load(loadable_card_path)

card_back_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\playing_cards\\card_back_scaled.png"))
hit_button_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\hit_button_s.png"))
stick_button_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\stick_button_s.png"))
bet_plus_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\bet_plus.png"))
bet_minus_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\bet_minus.png"))
next_round_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\next_round.png"))
continue_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\continue.png"))
cashout_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\cashout.png"))
restart_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\restart.png"))
quit_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "blackjack\\buttons\\quit.png"))

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode([screen_width, screen_height])

"""
Set up the width and height of our cards
Create a place for the cards to be drawn (card_placer), with our with and height
"""
card_w = 64
card_h = 89
times_to_shuffle = 100
card_placer = pygame.Surface((card_w, card_h))

class GameState(Enum):  #   A list of states the game can be in. A general view of whats happening
    GS_INIT = 0
    GS_BET = 1
    GS_PLAYER_TURN = 2
    GS_DEALER_TURN = 3
    GS_END_ROUND = 4
    GS_QUIT = 6

state_updated = False
def change_state(new_state):
    global game_state
    global state_updated

    game_state = new_state
    state_updated = True

class Button:
    def __init__(self, position, sprite, func):
        self.pos = position
        self.image = sprite
        self.callback = func
        self.active = False
        return
    
    def render(self):
        global screen
        screen.blit(self.image, self.pos)
        return
    
    def click_check(self):
        """
        checking the position of the mouse
        this checks an x (pos[0]) and y (pos[1]) coordinate for the mouse,
        against the x (self.pos[0]) and y (self.pos[1]) coordinates of this button
        the button starts at self.pos[0]  and ends at (self.pos[0] + button_width), similarly for height
        """
        if self.active:
            pos = pygame.mouse.get_pos()
            if (pos[0] > self.pos[0] and    #check mouse is further than the start of this button
                pos[0] < (self.pos[0] + button_width) and   #and check is is not further than the end
                pos[1] > self.pos[1] and
                (pos[1] < (self.pos[1] + button_height))):

                """
                self.callback() is set as hit_clicked when creating the hit_button.
                this allows us to call a function (hit_clicked())
                """
                self.callback() #callback = hit_clicked   so   callback() = hit_clicked()
        return

button_height = 32
button_width = 128
button_spacing = 4

"""
Positioning relative to the screen.
This probably wont scale well, as image sizes will not grow and shrink with the screen size
"""
current_btn_txt_offset = (((screen_width / 4) * 3), (screen_height / 2) - bet_text_texture.get_height() - money_text_texture.get_height() - (button_height + ((7 * button_spacing) / 2)))

money_text_pos = current_btn_txt_offset

bet_text_pos = (current_btn_txt_offset[0], current_btn_txt_offset[1] + button_spacing + bet_text_texture.get_height())
current_btn_txt_offset = bet_text_pos

hit_button_pos = (current_btn_txt_offset[0], current_btn_txt_offset[1] + button_spacing + button_height)
current_btn_txt_offset = hit_button_pos

stick_button_pos = (current_btn_txt_offset[0], current_btn_txt_offset[1] + button_spacing + button_height)
current_btn_txt_offset = stick_button_pos

next_round_button_pos = (current_btn_txt_offset[0], current_btn_txt_offset[1] + button_spacing + button_height)

deck = []
def deal_card():
    global deck     #   grab that deck
    if len(deck) > 0:   #   make sure we have a card left
        return deck.pop()   #   take one off deck and return it
    else:
        pass    #   handle soon

def hit_clicked(dealer = False):
    global bet_increment
    global player
    global dealer_timer
    global dealer_delay
    cPrintClear()
    if not dealer:
        cPrint("Hit clicked")
        hand = player.hand
        stats["total_cards_dealt"] = stats["total_cards_dealt"] + 1
    else:
        cPrint("Dealer Hit")
        hand = dealer_hand
    hand.add_card(deal_card())

    if(hand.value == 0):
        if not dealer:
            cPrint("Bust")
            player.current_bet = bet_increment
            update_money_text()
            update_stat("losses", stats["losses"] + 1)
        else:
            cPrint("Dealer Bust")
            player.money += player.current_bet * 2
            update_stat("wins", stats["wins"] + 1)
            update_money_text()
            check_money_stats()
        change_state(GameState.GS_END_ROUND)
    elif hand.value == 21: #   21, no need to hit, move to dealers turn
        if not dealer:
            cPrint("21")
            dealer_timer = dealer_delay + pygame.time.get_ticks()
            change_state(GameState.GS_DEALER_TURN)
        else:
            cPrint("Dealer 21")
            if player.hand.value < 21:
                player.current_bet = bet_increment
                update_stat("losses", stats["losses"] + 1)
            elif player.hand.value == 21:
                cPrint("Push")
                player.money += player.current_bet
                update_stat("pushes", stats["pushes"] + 1)
                update_money_text()
            change_state(GameState.GS_END_ROUND)
    else:   #   below 21, can still hit
        if not dealer:
            cPrint("Hand: " + str(player.hand.value))
        else:
            cPrint("Dealer Hand: " + str(dealer_hand.value))
        if(len(hand.cards) == 5) and not dealer:    #   5 card trick
            cPrint("5 card trick!")
            update_stat("5_card_tricks", stats["5_card_tricks"] + 1)
            player.money += player.current_bet * 2
            change_state(GameState.GS_END_ROUND)
    return

def stick_clicked():
    cPrintClear()
    cPrint("Stick on " + str(player.hand.value))
    change_state(GameState.GS_DEALER_TURN)
    return

def bet_plus_clicked():
    global player
    cPrintClear()
    if (player.current_bet + bet_increment) <= player.money:
        cPrint("Bet + " + str(bet_increment))
        player.current_bet += bet_increment
    else:
        cPrint("Not enough money to increase bet by " + str(bet_increment))
    update_money_text()
    return

def bet_minus_clicked():
    global player
    cPrintClear()
    if player.current_bet > bet_increment:
        cPrint("Bet - " + str(bet_increment))
        player.current_bet -= bet_increment
    else:
        cPrint("Bet cannot be below " + str(bet_increment))
    update_money_text()
    return

def check_money_stats():
    global player
    global stats
    if player.money > stats["max_money"]:
        update_stat("max_money", player.money)
    elif player.money < stats["min_money"]:
        update_stat("min_money", player.money)
    if player.current_bet > stats["max_bet"]:
        update_stat("max_bet", player.current_bet)
    elif player.current_bet < stats["min_bet"]:
        update_stat("min_bet", player.current_bet)
    return

def next_round_clicked():
    global stats
    cPrintClear()
    cPrint("Next Round")
    player.money -= player.current_bet
    if player.first_hand:
        update_stat("min_bet", player.current_bet)
        update_stat("max_bet", player.current_bet)
        player.first_hand = False
    update_money_text()
    check_money_stats()
    
    update_stat("total_hands", stats["total_hands"] + 1)
    change_state(GameState.GS_PLAYER_TURN)
    return

def continue_clicked():
    cPrintClear()
    change_state(GameState.GS_BET)
    return

def restart_clicked():
    cPrintClear()
    change_state(GameState.GS_INIT)
    return

def cashout_clicked():
    cPrintClear()
    change_state(GameState.GS_QUIT)
    return

def quit_clicked():
    change_state(GameState.GS_QUIT)
    return

hit_button = Button(hit_button_pos, hit_button_img, hit_clicked)
stick_button = Button(stick_button_pos, stick_button_img, stick_clicked)

bet_plus_button = Button(hit_button_pos, bet_plus_img, bet_plus_clicked)
bet_minus_button = Button(stick_button_pos, bet_minus_img, bet_minus_clicked)
next_round_button = Button(next_round_button_pos, next_round_img, next_round_clicked)

continue_button = Button(hit_button_pos, continue_img, continue_clicked)
cashout_button = Button(stick_button_pos, cashout_img, cashout_clicked)

restart_button = Button(hit_button_pos, restart_img, restart_clicked)
quit_button = Button(stick_button_pos, quit_img, quit_clicked)

starting_money = 100
bet_increment = 10

"""
The offset is where we will start drawin the player and dealer hands
The positions are evenly spaced from the start position
Max 5 cards per hand, as that leads to 5 card trick
"""
card_spacing = 5
player_hand_offset = (((screen_width / 2) - (card_w * 2.5)) - (2 * card_spacing), ((screen_height / 4) * 3))
player_card_positions = (player_hand_offset,
                         (player_hand_offset[0] + card_w + card_spacing, player_hand_offset[1]),
                         (player_hand_offset[0] + ((card_w + card_spacing) * 2), player_hand_offset[1]),
                         (player_hand_offset[0] + ((card_w + card_spacing) * 3), player_hand_offset[1]),
                         (player_hand_offset[0] + ((card_w + card_spacing) * 4), player_hand_offset[1]))

dealer_hand_offset = (((screen_width / 2) - (card_w * 2.5)) - (2 * card_spacing), (screen_height / 4) - card_h)
dealer_card_positions = (dealer_hand_offset,
                         (dealer_hand_offset[0] + card_w + card_spacing, dealer_hand_offset[1]),
                         (dealer_hand_offset[0] + ((card_w + card_spacing) * 2), dealer_hand_offset[1]),
                         (dealer_hand_offset[0] + ((card_w + card_spacing) * 3), dealer_hand_offset[1]),
                         (dealer_hand_offset[0] + ((card_w + card_spacing) * 4), dealer_hand_offset[1]))

class Hand():
    def __init__(self) -> None:
        self.cards = []
        self.value = 0
    def add_card(self, card_index):
        self.cards.append(card_index)
        self.value = self.check_hand()
    def print_cards(self):
        for card in self.cards:
            print(card)
    def check_hand(self):
        hand_val = 0
        aces = 0
        for card in self.cards:
            card_index = card % 13
            if card_index == 12:    #   ace - special case
                aces += 1           #   keep a total, and choose 1's or 11's later
                hand_val += 1       #   we'll add the 1 now, and maybe 10 later
            elif card_index < 9:    #   2-10  -  our sprites start at 2, so we add 2 to the index for value
                hand_val += card_index + 2
            else:                   #   all face cards = 10
                hand_val += 10
        if hand_val > 21:   #   Bust
            return 0
        elif hand_val < 12: #   Low enough to convert an ace up to 11
            if aces > 0:    #   as long as we have one
                hand_val += 10
                if hand_val == 21:  #   bang on 21
                    if len(self.cards) == 2:  #   only 2 cards, blackjack!!
                        return -1
        return hand_val
        # return_vals   0 - bust, -1 - blackjack, N - hand_value (2 - 21)

class Player():
    def __init__(self):
        self.money = starting_money
        self.current_bet = bet_increment
        self.hand = Hand()
        self.first_hand = True
        return

stats = {
    "min_money" : 0,
    "max_money" : 0,
    "min_bet" : 0,
    "max_bet" : 0,

    "total_hands" : 0,
    "average_hands" : 0,
    "blackjacks" : 0,
    "5_card_tricks" : 0,
    
    "total_cards_dealt" : 0,
    "wins" : 0,
    "losses" : 0,
    "pushes" : 0
}

def update_stat(stat, new_val):
    global stats
    if stat in stats:
        stats[stat] = new_val
    else:
        cPrint("Invalid stat to update: " + stat)
    return

def render_stats():
    global stats
    global screen

    i = 0
    text_offset = ((screen_width / 6), screen_height / 2)
    for stat, val in stats.items():
        text_string = stat + ": " + str(val)
        text_texture = font.render(text_string, True, (0,0,0))
        
        width_offset = (i // 4) * ((screen_width / 6) + 32)
        height_offset = (-2) + (i % 4)
        text_pos = (text_offset[0] + width_offset, text_offset[1] + (height_offset * text_texture.get_height()))
        
        screen.blit(text_texture, text_pos)
        i += 1
    return

player = Player()   # This player has money, a current_bet and a hand
dealer_hand = Hand()
dealer_delay = 2000  #   ms. 2 seconds
dealer_timer = 0
change_state(GameState.GS_INIT)

def index_to_val(index):
    card_num = index % 13   #   cycle through suits, only find val 0 - 13

def shuffle_deck():
    global deck     # grab our deck
    deck = [x for x in range(52)]       #   stick 52 new cards in there
    for i in range(times_to_shuffle):
        random.shuffle(deck)    #   shuffle that badboy
    return

def hit_stick_buttons_active(state):
    hit_button.active = state
    stick_button.active = state
    return

def bet_buttons_active(state):
    bet_plus_button.active = state
    bet_minus_button.active = state
    next_round_button.active = state
    return

def continue_buttons_active(state):
    continue_button.active = state
    cashout_button.active = state
    return

def restart_buttons_active(state):
    restart_button.active = state
    quit_button.active =state
    return

def update_game():
    """
    We need to keep grabbing the global stuff here
    or python thinks we want to make new ones
    then everything stops working
    """
    global game_state
    global dealer_hand
    global player
    global state_updated
    global dealer_timer
    global dealer_delay
    global stats

    state_updated = False   #   reset this now we are dealing with it

    match game_state:
        case GameState.GS_INIT:
            """
            we reset everything here
            clear and re-shuffle the deck (which creates a new set of 52)
            and draw 2 cards for the player and dealer
            """
            player = Player()
            dealer_hand = Hand()
            update_money_text()

            hit_stick_buttons_active(False)
            bet_buttons_active(False)
            continue_buttons_active(False)
            restart_buttons_active(False)

            change_state(GameState.GS_BET)
            cPrintClear()
            return
        case GameState.GS_BET:
            hit_stick_buttons_active(False)
            bet_buttons_active(True)
            continue_buttons_active(False)
            restart_buttons_active(False)
            cPrint("Current Bet: " + str(player.current_bet))
            return
        case GameState.GS_PLAYER_TURN:
            hit_stick_buttons_active(True)
            bet_buttons_active(False)
            continue_buttons_active(False)
            restart_buttons_active(False)

            player.hand = Hand()
            dealer_hand = Hand()

            shuffle_deck()

            player.hand.add_card(deal_card())
            player.hand.add_card(deal_card())
            dealer_hand.add_card(deal_card())
            dealer_hand.add_card(deal_card())
            cPrintClear()
            if player.hand.value == -1:
                stats["blackjacks"] = stats["blackjacks"] + 1
                if dealer_hand.value == -1:
                    cPrint("Push! Double Blackjack!")
                    player.money += player.current_bet
                    update_money_text()
                else:
                    cPrint("Hand: Blackjack!")
                    player.money += int(player.current_bet * 1.5)
                    update_money_text()
                    check_money_stats()
            else:
                cPrint("Hand: " + str(player.hand.value))
            return
        case GameState.GS_DEALER_TURN:
            hit_stick_buttons_active(False)
            bet_buttons_active(False)
            continue_buttons_active(False)
            restart_buttons_active(False)
            """
            We're creating a timer here. it will start at 2 seconds, 2000 ms.
            it will decrease by the time since we were last here in the else clause below
            This is to control how fast the dealer makes move, to keep it visible.
            """
            if(dealer_timer <= pygame.time.get_ticks()):
                dealer_timer = dealer_delay + pygame.time.get_ticks()
                if dealer_hand.value > player.hand.value:
                    cPrint("Dealer wins: " + str(dealer_hand.value))
                    player.current_bet = bet_increment
                    update_money_text()
                    change_state(GameState.GS_END_ROUND)
                elif dealer_hand.value == player.hand.value:
                    cPrint("Push: Bet returned.")
                    player.money += player.current_bet
                    update_money_text()
                    change_state(GameState.GS_END_ROUND)
                elif dealer_hand.value < 17:
                    hit_clicked(True)   #   Dealer hits
                    state_updated = True    #   come back for another round
                elif dealer_hand.value == 17 and len(dealer_hand.cards) == 2:
                    hit_clicked(True)
                else:
                    cPrint("Dealer sticks on " + str(dealer_hand.value))
                    if player.hand.value > dealer_hand.value:
                        cPrint("Player wins!")
                        player.money += player.current_bet * 2
                        update_money_text()
                    elif player.hand.value == dealer_hand.value:
                        cPrint("Push")
                        player.money += player.current_bet
                        update_money_text()
                    else:
                        cPrint("Dealer wins.")
                    change_state(GameState.GS_END_ROUND)
            else:
                state_updated = True    #   continue waiting for next move
        case GameState.GS_END_ROUND:
            avg_hand = stats["average_hands"] * (stats["total_hands"] - 1)
            avg_hand += player.hand.value
            avg_hand /= stats["total_hands"]
            hit_stick_buttons_active(False)
            bet_buttons_active(False)
            continue_buttons_active(False)
            restart_buttons_active(False)
            if player.money > 0:
                cPrint("Another Round?")
                continue_buttons_active(True)
            else:
                cPrint("Restart?")
                restart_buttons_active(True)
        case GameState.GS_QUIT:
            return
    return

def render_card(index, dest):   #   Draws a single card
    """
    Were going to take the index of a card (index)
    and the destination for where we draw it (dest)
    """
    sprite_area = (card_w*((index % 13)), card_h*(index // 13), card_w, card_h)
    """
    we find the width of a card (card_w)
    and find how many cards along we are (index % 13)
        this will start back at 0 every 13 cards.
        allowing us to cycle through all 4 suits
        we use this as an x coordinate, on the cards_scaled image

    with the height (card_h) we find how many suits we have passed through (index // 13)
        this will increase by 1 for every 13 card we have passed
        we use this as the y coordinate
    """
    card_placer.blit(card_spritesheet, (0,0), sprite_area)  #   draw our card to the card_placer
    if index == -1:
        screen.blit(card_back_img, dest, (0, 0, card_w, card_h))    #   draw a card back, not front
    else:
        #   we scale our card placer, and draw it at dest
        screen.blit(pygame.transform.scale(card_placer, (card_w, card_h)), dest, (0, 0, card_w, card_h))

def render_cards(): #   draw all cards, calls draw_card() for each card
    global player   #   grab those globals
    global dealer_hand
    i = 0
    for card_p in player.hand.cards:  #   cycle the players hand
        render_card(card_p, player_card_positions[i])   #   draw each card
        i += 1
    i = 0
    if game_state == GameState.GS_DEALER_TURN or game_state == GameState.GS_END_ROUND:  #   if its the dealers turn
        for card_d in dealer_hand.cards:
            render_card(card_d, dealer_card_positions[i])   #   then show all of his cards
            i += 1
    else:                                       #   but if its not the dealers turn
        render_card(dealer_hand.cards[0], dealer_card_positions[0])   #   only show his first card
        render_card(-1, dealer_card_positions[1])

def render():
    global screen
    screen.fill((200, 200, 200))    #   if you dont fill the screen, all the old stuff will stay there
    if game_state != GameState.GS_BET and game_state != GameState.GS_INIT and game_state != GameState.GS_QUIT:
        render_cards()
        if game_state == GameState.GS_PLAYER_TURN:  #   only draw these buttons on the players turn
            hit_button.render()
            stick_button.render()
        if game_state == GameState.GS_END_ROUND:
            if player.money > 0:
                continue_button.render()
                cashout_button.render()
            else:
                restart_button.render()
                quit_button.render()
    if game_state == GameState.GS_BET:
        bet_plus_button.render()
        bet_minus_button.render()
        next_round_button.render()
    
    if game_state != GameState.GS_QUIT:
        global text
        screen.blit(text_texture, ((screen_width - text_texture.get_width()) / 5, (screen_height - text_texture.get_height()) / 2))
        screen.blit(money_text_texture, money_text_pos)
        screen.blit(bet_text_texture, bet_text_pos)
    else:
        render_stats()
    pygame.display.flip()
    return

def click_check_buttons():
    if game_state == GameState.GS_PLAYER_TURN:
        hit_button.click_check()
        stick_button.click_check()
    if game_state == GameState.GS_BET:
        bet_plus_button.click_check()
        bet_minus_button.click_check()
        next_round_button.click_check()
    if game_state == GameState.GS_END_ROUND:
        if player.money > 0:
            continue_button.click_check()
            cashout_button.click_check()
        else:
            restart_button.click_check()
            quit_button.click_check()
    return


def main():
    random.seed(time.time())    # use the current time for a random random
    running = True  # keeps the game running
    global game_state   # keeps track of what part of the game were in
    game_state = GameState.GS_INIT
    while(running):
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    change_state(GameState.GS_INIT) # Pressed spacebar - K_SPACE.  Re-start the game.
            elif event.type == pygame.MOUSEBUTTONUP:    # mouse has been clicked, check if its on a button
                click_check_buttons()
        #update
        if(state_updated):  #   if we have updated the game state
            update_game()   # Checks the game state, and updates accordingly
        #render
        render()    # Draw things to the screen
    
    pygame.quit()
    return

main()