__author__ = "Mika Wainer"

import pygame
from os.path import dirname, join, exists, getsize, realpath, split, sys
import re
import time
from pygame import font

pygame.init()
font.init()

GOLD = (229, 193, 0)

def is_pressed(rect, mouse):
    """
    check if mouse on rect
    """
    if mouse[0] > rect.topleft[0]:
        if mouse[1] > rect.topleft[1]:
            if mouse[0] < rect.bottomright[0]:
                if mouse[1] < rect.bottomright[1]:
                    return True
    return False

class Menu():
    def __init__(self, screen, menu, font_name='Birdy Game.ttf', font_size=25, font_color=(0,0,0)):
        path = dirname(__file__)
        self.screen = screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        self.font = font.Font(join(path,font_name),font_size)
        self.font_color = font_color
        self.item_spacing = 20
        self.menu = self.create_menu(menu)
    
    def create_button(self, color, font_height, (x,y) = (60,60), rect_len = 180):
        height = font_height + 5*2
        tri_len = rect_len/4
        rect_len += 5*2
        x -= (tri_len + 5)
        y -= 5
        pygame.draw.polygon(self.screen, color, ((x + tri_len, y), (x, y + height/2), (x + tri_len, y + height)))
        pygame.draw.rect(self.screen, color, (x + tri_len, y, rect_len, height), 0)
        pygame.draw.polygon(self.screen, color, ((x + tri_len + rect_len, y), (x + tri_len*2 + rect_len, y + height/2), (x + tri_len + rect_len, y + height)))
        #pygame.draw.line(windowSurface, BLUE, (x + 60*2 + 60, y), (x + 60*2 + 60, y + 60), 4)
    
    def create_menu(self, items):
        """
        list of [text, type(str),width(int),height(int),pos_x(int), pos_y(int)]
        type = BUTTON
        """
        menu = []
        ttl_height = 0
        for item in items:
            label = self.font.render(item,1,self.font_color)
            label_width = label.get_rect().width
            label_height = label.get_rect().height
            pos_X = (self.width / 2) - (label_width / 2)
            menu.append([item, label_width, label_height, pos_X])
            ttl_height += label_height
        pos_Y = (self.height - (ttl_height + self.item_spacing*(len(items) -1)))/2
        for item in menu:
            item.append(pos_Y)
            pos_Y += item[2] + self.item_spacing
        return menu
    
    def print_menu(self, menu):
        print "\n".join(str(item) for item in menu)
    
    def add_text(self,item):
        """
        get an item -> [text, type(str)="TEXT",width(int),height(int),pos_x(int), pos_y(int)]
        fun only use the [text,pos_x,pos_y]
        """
        label = self.font.render(item[0], 1, self.font_color)
        self.screen.blit(label, (item[3], item[4]))
    
    def draw_menu(self, button_color = GOLD):
        for item in self.menu:
            self.create_button(button_color, item[2], (item[3], item[4]), item[1])
            self.add_text(item)

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')
    screen.fill((0,0,142))
    game_menu = Menu(screen, ["log in", "play", "setting", "quit"])
    game_menu.draw_menu()
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()