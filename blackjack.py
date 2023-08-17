import pygame
import random
import time
from enum import Enum
import os
pygame.init()

card_path = "blackjack\\playing_cards\\cards_scaled.png"
card_back_path = "blackjack\\playing_cards\\card_back_scaled.png"
card_spritesheet = pygame.image.load(os.path.join(os.path.dirname(__file__), card_path))
card_back_img = pygame.image.load(os.path.join(os.path.dirname(__file__), card_back_path))

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode([screen_width, screen_height])

hit_button_path = "blackjack\\buttons\\hit_button.png"
stick_button_path = "blackjack\\buttons\\stick_button.png"

card_w = 64
card_h = 89
times_to_shuffle = 100
card_placer = pygame.Surface((card_w, card_h))
class GameState(Enum):
    GS_INIT = 0
    GS_PLAYER_TURN = 1
    GS_DEALER_TURN = 2
    GS_END_ROUND = 3
    GS_GAME_OVER = 4

class Button:
    def __init__(self, position, sprite, func):
        self.pos = position
        self.image = sprite
        self.callback = func
        self.active = False
    def render(self):
        global screen
        screen.blit(self.image, self.pos)

hit_button_height = 32
hit_button_width = 128
stick_button_height = 32
stick_button_width = 128
button_spacing = 4
hit_button_pos = (((screen_width / 4) * 3), (screen_height / 2) - (hit_button_height + (button_spacing / 2)))
stick_button_pos = (((screen_width / 4) * 3), (screen_height / 2) + (button_spacing / 2))

hit_button_path = "blackjack\\buttons\\hit_button_s.png"
stick_button_path = "blackjack\\buttons\\stick_button_s.png"

hit_button_img = pygame.image.load(os.path.join(os.path.dirname(__file__), hit_button_path))
stick_button_img = pygame.image.load(os.path.join(os.path.dirname(__file__), stick_button_path))

def hit_clicked():
    pass

def stick_clicked():
    pass

hit_button = Button(hit_button_pos, hit_button_img, hit_clicked)
stick_button = Button(stick_button_pos, stick_button_img, stick_clicked)

starting_money = 100

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
class Player():
    money = starting_money
    current_bet = 0
    hand = []

player = Player()
deck = []
dealer_hand = []
game_state = GameState.GS_INIT

def int_to_suit(num):
    match num:
        case 0:
            return "clubs"
        case 1:
            return "diamonds"
        case 2:
            return "hearts"
        case 3:
            return "spades"

def shuffle_deck():
    global deck
    deck = [x for x in range(52)]
    for i in range(times_to_shuffle):
        random.shuffle(deck)
    return

def deal_card(hand):
    global deck
    hand.append(deck.pop())
    return

def betting_buttons_active(state):
    hit_button.active = state
    stick_button.active = state

def update_game():
    global game_state
    global dealer_hand
    global player
    match game_state:
        case GameState.GS_INIT:
            player.money = starting_money
            player.hand = []
            player.current_bet = 0
            dealer_hand = []
            #intro
            shuffle_deck()
            #deal cards
            deal_card(player.hand)
            deal_card(player.hand)
            deal_card(dealer_hand)
            deal_card(dealer_hand)
            game_state = GameState.GS_PLAYER_TURN
            return
        case GameState.GS_PLAYER_TURN:
            betting_buttons_active(True)
            return
        case GameState.GS_DEALER_TURN:
            pass
        case GameState.GS_END_ROUND:
            pass
        case GameState.GS_GAME_OVER:
            pass
    return

def render_card(index, dest):
    sprite_area = (card_w*((index % 13)), card_h*(index // 13), card_w, card_h)
    #sprite_area = ((256*12), 356*3, 256, 356)
    card_placer.blit(card_spritesheet, (0,0), sprite_area)
    if index == -1:
        screen.blit(card_back_img, dest, (0, 0, card_w, card_h))
    else:
        screen.blit(pygame.transform.scale(card_placer, (card_w, card_h)), dest, (0, 0, card_w, card_h))

def render_cards():
    global player
    global dealer_hand
    i = 0
    for card_p in player.hand:
        render_card(card_p, player_card_positions[i])
        i += 1
    i = 0
    if game_state == GameState.GS_DEALER_TURN:
        for card_d in dealer_hand:
            render_card(card_d, dealer_card_positions[i])
            i += 1
    else:
        render_card(dealer_hand[0], dealer_card_positions[0])
        render_card(-1, dealer_card_positions[1])

def render():
    global screen
    screen.fill((200, 200, 200))
    render_cards()
    if game_state == GameState.GS_PLAYER_TURN:
        hit_button.render()
        stick_button.render()
    
    pygame.display.flip()

def main():
    random.seed(time.time())
    running = True
    global game_state
    while(running):
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass
                if event.key == pygame.K_SPACE:
                    game_state = GameState.GS_INIT
        #update
        update_game()

        #render
        render()
    
    pygame.quit()
    return

main()