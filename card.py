import pygame

from config import *

class Card(pygame.sprite.Sprite):
    def __init__(self, colour, number):
        super().__init__()
        self.colour = colour
        self.number = number
        self.is_selected = False
        self.parent_set = None

    def __repr__(self):
        return f"Card({self.colour} {self.number})"
        
    # Update a sprite
    # Pygame Display object, Tuple(position_x, position_y) -> None
    def draw(self, game_engine):
        if self.is_selected:
            # border = pygame.draw.rect(game_engine.screen, (0, 255, 255), self.rect, width=500, border_radius=1)
            self.rect.x += 10
            self.rect.y += 10
            pygame.draw.rect(game_engine.screen, (255, 0, 0), self.rect, 10)
            game_engine.screen.blit(self.image, (self.rect.x + 5, self.rect.y + 5)) 
            print("something1")
        else:
            game_engine.screen.blit(self.image, (self.rect.x, self.rect.y))
            print("something2")
        pygame.display.update()
    
    # Perfome actions when the card is clicked
    # Game engine instance -> None
    def left_click_action(self,game_engine):
        current_player = game_engine.turn
        # Actions if the card belongs to a set
        if self.parent_set:
            current_player.selected.append(self.parent_set) 
            print(current_player.selected)
            self.parent_set.highlight(game_engine)
        # Add itself to the list of selected cards
        else:
            current_player.selected.append(self)
            print(current_player.selected)
            
            self.highlight(game_engine)

    # Perfome actions when the card is clicked
    # Game engine instance -> None
    def right_click_action(self,game_engine):
        current_player = game_engine.turn
        # Move to a set
        if self.parent_set:
            current_player.selected.append(self.parent_set) 
            current_player.make_move(game_engine)
        else:
            current_player.selected.append(self)
            current_player.make_move(game_engine)

    # Highlight the card or unhighlight the card
    def highlight(self,game_engine):
        self.is_selected = not self.is_selected
        self.draw(game_engine)

    # Get only the colour cards for a pack of cards
    # None -> List[ColourCard]
    @staticmethod
    def get_colour_cards(cards):
        return [colour_card for colour_card in cards if isinstance(colour_card, ColourCard)]

    # Get only the Joker cards for a pack of cards
    # None -> List[JokerCard]
    @staticmethod
    def get_joker_cards(cards):
        return [joker_card for joker_card in cards if isinstance(joker_card, JokerCard)]
    

class ColourCard(Card):
    def __init__(self, colour, number):
        super().__init__(colour, number)
        self.joker = False
        self.image = pygame.transform.smoothscale(pygame.image.load(f"./src/{self.colour.lower()}{self.number}.png"), (90,120))
        self.rect = self.image.get_rect()

    # Get the penalty for this card 
    # None -> int
    def penalty(self):
        # Need to be implemented
        pass

class JokerCard(Card):
    def __init__(self):
        super().__init__(None, None)
        self.joker = True
        self.image = pygame.transform.smoothscale(pygame.image.load(f"./src/joker.png"), (90,120))
        self.rect = self.image.get_rect()
    
    # Get the penalty for this card 
    # None -> int
    def penalty(self):
        return -30