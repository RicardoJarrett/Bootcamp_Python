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
pygame.init()
font = pygame.font.SysFont('arial', 15)
text = ""
text_texture = font.render(text, True, (0,0,0))

def cPrint(in_text):
    global text
    global text_texture
    text += " " + in_text
    text_texture = font.render(text, True, (0,0,0))

def cPrintClear():
    global text
    global text_texture
    text = ""
    text_texture = font.render("", True, (0,0,0))

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
    GS_PLAYER_TURN = 1
    GS_DEALER_TURN = 2
    GS_END_ROUND = 3
    GS_GAME_OVER = 4

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
    def render(self):
        global screen
        screen.blit(self.image, self.pos)
    def click_check(self):
        """
        checking the position of the mouse
        this checks an x (pos[0]) and y (pos[1]) coordinate for the mouse,
        against the x (self.pos[0]) and y (self.pos[1]) coordinates of this button
        the button starts at self.pos[0]  and ends at (self.pos[0] + button_width), similarly for height
        """
        pos = pygame.mouse.get_pos()
        if (pos[0] > self.pos[0] and    #check mouse is further than the start of this button
            pos[0] < (self.pos[0] + button_width) and   #and check is is not further than the end
            pos[1] > self.pos[1] and
            (pos[1] < (self.pos[1] + button_height))):

            """
            self.callback() is set as hit_clicked when creating the hit_button.
            this allows us to call a function (hit_clicked())
            """
            cPrintClear()
            self.callback() #callback = hit_clicked   so   callback() = hit_clicked()

button_height = 32
button_width = 128
button_spacing = 4

"""
Positioning relative to the screen.
This probably wont scale well, as image sizes will not grow and shrink with the screen size
"""
hit_button_pos = (((screen_width / 4) * 3), (screen_height / 2) - (button_height + (button_spacing / 2)))
stick_button_pos = (((screen_width / 4) * 3), (screen_height / 2) + (button_spacing / 2))

deck = []
def deal_card():
    global deck     #   grab that deck
    if len(deck) > 0:   #   make sure we have a card left
        return deck.pop()   #   take one off deck and return it
    else:
        pass    #   handle soon

def hit_clicked():
    global player
    cPrint("Hit clicked")
    player.p_hand.add_card(deal_card())
    if(player.p_hand.value == 0):
        cPrint("Bust")
        change_state(GameState.GS_INIT)
    elif player.p_hand.value == 21: #   21, no need to hit, move to dealers turn
        cPrint("21")
        change_state(GameState.GS_DEALER_TURN)
    else:
        cPrint("Hand: " + str(player.p_hand.value))
        if(len(player.p_hand.cards) == 5):
            cPrint("5 card trick!")
            change_state(GameState.GS_INIT)
        pass    #   below 21, can still hit

def stick_clicked():
    cPrint("Stick clicked")
    change_state(GameState.GS_DEALER_TURN)

hit_button = Button(hit_button_pos, hit_button_img, hit_clicked)
stick_button = Button(stick_button_pos, stick_button_img, stick_clicked)

starting_money = 100

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
    money = starting_money
    current_bet = 0
    p_hand = Hand()
    def reset(self):
        self.money = starting_money
        self.current_bet = 0
        self.p_hand = Hand()

player = Player()   # This player has money, a current_bet and a hand
dealer_hand = Hand()
change_state(GameState.GS_INIT)

def index_to_val(index):
    card_num = index % 13   #   cycle through suits, only find val 0 - 13

def shuffle_deck():
    global deck     # grab our deck
    deck = [x for x in range(52)]       #   stick 52 new cards in there
    for i in range(times_to_shuffle):
        random.shuffle(deck)    #   shuffle that badboy
    return

def betting_buttons_active(state):
    hit_button.active = state
    stick_button.active = state

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
    state_updated = False   #   reset this now we are dealing with it

    match game_state:
        case GameState.GS_INIT:
            """
            we reset everything here
            clear and re-shuffle the deck (which creates a new set of 52)
            and draw 2 cards for the player and dealer
            """
            player.reset()
            dealer_hand = Hand()

            shuffle_deck()

            player.p_hand.add_card(deal_card())
            player.p_hand.add_card(deal_card())
            cPrint("Hand: " + str(player.p_hand.value))
            dealer_hand.add_card(deal_card())
            dealer_hand.add_card(deal_card())
            #   check the first hands for blackjack/s
            if(player.p_hand.value == -1):
                if(dealer_hand.value == -1):
                    pass    #   push, payout what was paid in
                else:
                    pass    #   win by blackjack!
            change_state(GameState.GS_PLAYER_TURN)
            return
        case GameState.GS_PLAYER_TURN:
            betting_buttons_active(True)
            return
        case GameState.GS_DEALER_TURN:
            betting_buttons_active(False)
            if dealer_hand.value > player.p_hand.value:
                pass    #   dealer wins
            elif dealer_hand.value == player.p_hand.value:
                pass    #   push
            elif dealer_hand.value < 17:
                pass    #   hit
            elif dealer_hand.value == 17 and len(dealer_hand.cards) == 2:
                pass    #   soft 17, hit
            else:
                pass    #   stick
            pass
        case GameState.GS_END_ROUND:
            pass
        case GameState.GS_GAME_OVER:
            pass
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
    for card_p in player.p_hand.cards:  #   cycle the players hand
        render_card(card_p, player_card_positions[i])   #   draw each card
        i += 1
    i = 0
    if game_state == GameState.GS_DEALER_TURN:  #   if its the dealers turn
        for card_d in dealer_hand.cards:
            render_card(card_d, dealer_card_positions[i])   #   then show all of his cards
            i += 1
    else:                                       #   but if its not the dealers turn
        render_card(dealer_hand.cards[0], dealer_card_positions[0])   #   only show his first card
        render_card(-1, dealer_card_positions[1])

def render():
    global screen
    screen.fill((200, 200, 200))    #   if you dont fill the screen, all the old stuff will stay there
    render_cards()
    if game_state == GameState.GS_PLAYER_TURN:  #   only draw these buttons on the players turn
        hit_button.render()
        stick_button.render()
    
    global text
    screen.blit(text_texture, ((screen_width - text_texture.get_width()) / 2, (screen_height - text_texture.get_height()) / 2))
    
    pygame.display.flip()

def main():
    random.seed(time.time())    # use the current time for a random random
    running = True  # keeps the game running
    global game_state   # keeps track of what part of the game were in
    while(running):
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    change_state(GameState.GS_INIT) # Pressed spacebar - K_SPACE.  Re-start the game.
            elif event.type == pygame.MOUSEBUTTONUP:    # mouse has been clicked, check if its on a button
                hit_button.click_check()
                stick_button.click_check()
        #update
        if(state_updated):  #   if we have updated the game state
            update_game()   # Checks the game state, and updates accordingly
        #render
        render()    # Draw things to the screen
    
    pygame.quit()
    return

main()