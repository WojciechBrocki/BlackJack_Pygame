import pygame as pygame
import json
from blackjack_deck import *
from constants import *
import sys
import time
pygame.init()

clock = pygame.time.Clock()

game_state = {
    'Wins' : 0,
    'ties' : 0,
    'loses' : 0
}
try:
    with open('save.txt') as save_file:
        game_state = json.load(save_file)
except:
    print('No save file yet')



gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('BlackJack')
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def end_text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()



def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

 
def game_finish(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def black_jack(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)


class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        
    def blackjack(self):

        self.dealer.calc_hand()
        self.player.calc_hand()
        try:
            show_dealer_card = pygame.image.load('Resources/' + self.dealer.card_img[1] + '.png').convert()
        except:
            return
        true_dealer_card = pygame.transform.scale(show_dealer_card, (100, 160))
        if self.player.value == 21 and self.dealer.value == 21:
            gameDisplay.blit(true_dealer_card, (550, 200))
            black_jack("Both with BlackJack!", 500, 250, grey)
            game_state['ties'] +=1
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            gameDisplay.blit(true_dealer_card, (550, 200))
            black_jack("You got BlackJack!", 500, 250, green)
            game_state['Wins'] +=1
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            gameDisplay.blit(true_dealer_card, (550, 200))
            black_jack("Dealer has BlackJack!", 500, 250, red)
            game_state['loses'] +=1
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0
        self.dealer.value = 0

    def deal(self):
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card_1 = pygame.image.load('resources/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_1_1 = pygame.transform.scale(dealer_card_1, (100, 160))
        dealer_card_2_1 = pygame.image.load('resources/back.png').convert()
        dealer_card_2_2 = pygame.transform.scale(dealer_card_2_1, (100, 160))
            
        player_card_1 = pygame.image.load('resources/' + self.player.card_img[0] + '.png').convert()
        player_card_1_1 = pygame.transform.scale(player_card_1, (100, 160))
        player_card_2 = pygame.image.load('resources/' + self.player.card_img[1] + '.png').convert()
        player_card_2_2 = pygame.transform.scale(player_card_2, (100, 160))

        
        game_texts("Dealer's hand is:", 500, 150)

        gameDisplay.blit(dealer_card_1_1, (400, 200))
        gameDisplay.blit(dealer_card_2_2, (550, 200))

        game_texts("Your's hand is:", 500, 400)
        
        gameDisplay.blit(player_card_1_1, (300, 450))
        gameDisplay.blit(player_card_2_2, (410, 450))
        self.blackjack()
            
            

    def hit(self):
        self.player.add_card(self.deck.deal())
        self.blackjack()
        try:
            self.player_card += 1
        except:
            return
        
        if self.player_card == 2:
            self.player.calc_hand()
            self.player.display_cards()
            try:
                player_card_3_1 = pygame.image.load('resources/' + self.player.card_img[2] + '.png').convert()
            except:
                return
            player_card_3_2 = pygame.transform.scale(player_card_3_1, (100, 160))
            gameDisplay.blit(player_card_3_2, (520, 450))

        if self.player_card == 3:
            self.player.calc_hand()
            self.player.display_cards()
            try:
                player_card_4_1 = pygame.image.load('resources/' + self.player.card_img[3] + '.png').convert()
            except:
                return
            player_card_4_2 = pygame.transform.scale(player_card_4_1, (100, 160))
            gameDisplay.blit(player_card_4_2, (630, 450))
                
        if self.player.value > 21:
            show_dealer_card_1_1 = pygame.image.load('resources/' + self.dealer.card_img[1] + '.png').convert()
            show_dealer_card_1_2 = pygame.transform.scale(show_dealer_card_1_1, (100, 160))
            gameDisplay.blit(show_dealer_card_1_2, (550, 200))
            game_finish("You Busted!", 500, 250, red)
            game_state['loses'] +=1
            time.sleep(4)
            self.play_or_exit()
            
        self.player.value = 0

        if self.player_card > 4:
            sys.exit()
            
            
    def stand(self):
        try:
            show_dealer_card_2_1 = pygame.image.load('resources/' + self.dealer.card_img[1] + '.png').convert()
        except:
            return
        try:
            show_dealer_card_2_2 = pygame.transform.scale(show_dealer_card_2_1, (100, 160))
        except:
            return
        gameDisplay.blit(show_dealer_card_2_2, (550, 200))
        self.blackjack()
        self.dealer.calc_hand()
        self.player.calc_hand()
        if self.player.value > self.dealer.value:
            game_finish("You Won!", 500, 250, green)
            game_state['Wins'] +=1
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value < self.dealer.value:
            game_finish("Dealer Wins!", 500, 250, red)
            game_state['loses'] +=1
            time.sleep(4)
            self.play_or_exit()
        else:
            game_finish("It's a Tie!", 500, 250, grey)
            game_state['ties'] +=1
            time.sleep(4)
            self.play_or_exit()
        
    
    def exit(self):
        with open('save.txt', 'w') as save_file:
                json.dump(game_state, save_file)
        sys.exit()
    
    def play_or_exit(self):
        game_texts("Play again press Deal!", 200, 50)
        time.sleep(3)
        self.player.value = 0
        self.dealer.value = 0
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()

        
play_blackjack = Play()

running = True




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('save.txt', 'w') as save_file:
                json.dump(game_state, save_file)
            running = False
        game_texts("wins: " + str(game_state['Wins']), 80, 100)
        game_texts("ties: " + str(game_state['ties']), 80, 150)
        game_texts("loses: " + str(game_state['loses']), 80, 200)
        button("Deal", 30, 320, 150, 50, light_slat, dark_slat, play_blackjack.deal)
        button("Hit", 30, 380, 150, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Stand", 30, 440, 150, 50, light_slat, dark_slat, play_blackjack.stand)
        button("EXIT", 30, 500, 150, 50, light_slat, dark_red, play_blackjack.exit)
    
    pygame.display.flip()
