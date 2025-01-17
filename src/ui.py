import pygame
from settings import *

class UI: 
    def __init__(self):
        
        # general 
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.endurance_bar_rect = pygame.Rect(10, 58, ENDURANCE_BAR_WIDTH, BAR_HEIGHT)
        
        # convert weapon dict 
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        # conver magic dict
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
    
    def show_bar(self, current, max_amount, bg_rect, colour):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, colour, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOUR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, text_rect.inflate(20, 12))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, text_rect.inflate(20, 12), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR_ACTIVE, bg_rect, 3)
        else: 
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)
        return bg_rect

    def overlay(self, overlay_index, has_switched,overlay_type):
        if overlay_type ==WEAPON:
            bg_rect = self.selection_box(10, 630, has_switched) # weapon
            overlay_surf = self.weapon_graphics[overlay_index]
        elif overlay_type ==MAGIC:
            bg_rect = self.selection_box(80, 635, has_switched)
            overlay_surf = self.magic_graphics[overlay_index]
        else:
            print('overlay type not found')
            return
        
        magic_rect = overlay_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(overlay_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOUR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOUR)
        self.show_bar(player.endurance, player.stats['endurance'], self.endurance_bar_rect, ENDURANCE_COLOUR)

        self.show_exp(player.exp)

        self.overlay(player.weapon_index, not player.can_switch_weapon,overlay_type=WEAPON)
        self.overlay(player.magic_index, not player.can_switch_magic,overlay_type=MAGIC)
