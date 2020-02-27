__author__ = "Mikey"

import pygame
from pygame import font, Rect
from os.path import dirname, join
import time

pygame.init()
font.init()

GOLD = (229, 193, 0)
WHITE = (255,255,255)
RETRO_BLUE = (0,0,142)
BLACK = (0,0,0)
LIGHT_BLUE = (47,180,219)
RETRO_DARK_LIGHT_BLUE = (10,35,117)
RETRO_DARK_SHADOW_BLUE = (8,8,102)
RETRO_SHADOW_BLUE = (64,96,129)
RETRO_DARK_BLUE = (13,107,135)
GREEN_GAME_TABLE = (49,79,79)

PATH = dirname(__file__)

class scrollbar():
    def __init__(self, rect, ratio, color=LIGHT_BLUE, alpha=150):
        self.scrollbar = Rect(rect)
        self.pos = (self.scrollbar.x, self.scrollbar.y)
        self.scrollbar.x = 0
        self.scrollbar.y = 0
        self.scrolling = False
        self.color = (color[0],color[1],color[2], alpha)
        self.line_color = color
        self.ratio = ratio
        self.keyboard_scrolling =0
        self.add = 0
    
    def draw(self, screen):
        new_screen = pygame.Surface((self.scrollbar.width, self.scrollbar.y + self.scrollbar.height), pygame.SRCALPHA)
        new_screen.fill((255,255,255,0))
        pygame.draw.rect(new_screen, self.color, self.scrollbar, 0)
        pygame.draw.rect(new_screen, self.line_color, self.scrollbar, 1)
        screen.blit(new_screen, (self.pos[0], self.pos[1] + self.scrollbar.y))
    
    def scrolling_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar.collidepoint((event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])):
                self.scrolling = True
            else:
                return False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.scrolling = False
        return True
    
    def event(self, event, screen_height):
        if self.scrolling:
            if event.type == pygame.MOUSEMOTION:
                if event.rel[1] != 0:
                    self.scrollbar.y += event.rel[1]
        if self.scrollbar.y < 0:
            self.scrollbar.y = 0
        elif 2*self.scrollbar.y + self.scrollbar.height > screen_height:
            self.scrollbar.y = 0.5*(screen_height - self.scrollbar.height)
        return False
    
    def run(self):
        screen = pygame.display.set_mode(ScrSize)
        world = pygame.Surface((ScrSize[0]*10, ScrSize[1]*10))
        screenRect = screen.get_rect()
        world.fill(Gray)
        for x in xrange(100, world.get_size()[0], 200):
            for y in xrange(100, world.get_size()[1], 200):
                pygame.draw.circle(world, Red, (x,y), 100, 10) 
        done = False
        screen_height = screen.get_height()
        ratio = float(screen_height) / world.get_height()
        scrollThick = 10
        self.scrollbar = pygame.Rect(screen.get_width() - scrollThick, 0, scrollThick, screen_height*ratio)
        
        while not done:
            screen.fill( (192,188,180) )
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif self.event(event, screen_height):
                    pass
                elif self.scrolling_event(event):
                    pass
            screen.blit(world, (0, (self.scrollbar.top / ratio) * -1))
            self.draw(screen)
            pygame.display.flip()

class retro_button():
    """button"""
    def __init__(self, text, button_pos=(0,0), text_font='FreePixel.ttf', font_size=25, margin=5, font_color=BLACK, color=RETRO_DARK_LIGHT_BLUE, alpha=120):
        font1 = font.Font(join(PATH,text_font), font_size)
        self.text = font1.render(text, 1, font_color)
        self.button_line_color = color
        self.button_color = (color[0],color[1],color[2],alpha)
        self.margin = margin
        self.set_pos(button_pos)
    
    def set_pos(self, (x, y)):
        text_width = self.text.get_rect().width
        text_height = self.text.get_rect().height
        
        self.rect = (x, y, text_width + 2*self.margin, text_height + 2*self.margin)
    
    def get_wh(self):
        return self.rect[2], self.rect[3]
    
    def draw_button(self, screen):
        screen_height = screen.get_rect().height
        screen_width = screen.get_rect().width
        new_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)   # per-pixel alpha
        new_screen.fill((255,255,255,0))
        
        pygame.draw.rect(new_screen, self.button_color, self.rect, 0)
        pygame.draw.rect(new_screen, self.button_line_color, self.rect, 1)
        
        screen.blit(new_screen, (0,0))
        screen.blit(self.text, (self.rect[0] + self.margin, self.rect[1] + self.margin))
    
    def is_pressed(self, mouse):
        """
        check if mouse on rect
        """
        rect = Rect(self.rect)
        if mouse[0] > rect.topleft[0]:
            if mouse[1] > rect.topleft[1]:
                if mouse[0] < rect.bottomright[0]:
                    if mouse[1] < rect.bottomright[1]:
                        return True
        return False
    
    def draw_background(self, screen):
        """
        draws background on screen (does not update screen)
        """
        screen.fill(BLACK)
        for y in range(0,screen.get_rect().height, 4):
            pygame.draw.line(screen, RETRO_DARK_BLUE, (0,y), (screen.get_rect().width, y), 1)
        #self.screen.blit(self.bg_image,self.bg_image.get_rect(center=self.screen.get_rect().center))
    
    def run(self):
        screen = pygame.display.set_mode((640, 480),pygame.SRCALPHA)
        pygame.display.set_caption('Game Menu')
        while 1:
            self.draw_background(screen)
            self.draw_button(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print self.is_pressed(pygame.mouse.get_pos())
            
            pygame.display.flip()

class status_window():
    """
    class pop up alert
    a status window will always appear at the center of the screen
    """
    def __init__(self, screen, title, text, text_font='FreePixel.ttf', title_size=25, text_size=15, frame_margin=50, inner_margin=10, frame_window_color=RETRO_DARK_SHADOW_BLUE,window_color=RETRO_DARK_LIGHT_BLUE, text_color=WHITE, title_alpha=230, text_alpha=230, scroll_thickness=10, scrollbar_color=LIGHT_BLUE, scrollbar_alpha=150):
        self.screen = screen
        self.background = pygame.Surface((screen.get_width(), screen.get_height()))
        self.background.blit(screen,(0,0))
        self.window_color = window_color
        self.frame_window_color = frame_window_color
        self.margin = inner_margin
        
        if not title:
            pass
        font1 = font.Font(join(PATH,text_font), title_size)
        font1.set_bold(True)
        self.title_surface = self.set_surface(title, text_color, font1, frame_margin, inner_margin)
        
        if not text:
            pass
        font1 = font.Font(join(PATH, text_font),text_size)
        self.text_surface = self.set_surface(text, text_color, font1, frame_margin, inner_margin)
        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        window_width = 0.5*(0.5*screen_width - frame_margin - inner_margin)
        window_height = 0.5*(screen_height - frame_margin - self.title_surface.get_height() - self.text_surface.get_height() - 3*inner_margin)
        
        if window_height < 0:
            window_height = frame_margin
        self.title_surface_position = (window_width/2,window_height)
        self.text_surface_position = (window_width/2,window_height + self.title_surface.get_height() +2*inner_margin)
        
        self.title_surface_alpha = title_alpha
        self.text_surface_alpha = text_alpha
        
        self.is_scrollbar = False
        self.set_title_surface(frame_margin)
        if self.is_scrollbar:
            self.text_surface = self.set_surface(text, text_color, font1, frame_margin, self.margin*2)
            self.set_scrollbar(frame_margin, scroll_thickness, scrollbar_color, scrollbar_alpha)
    
    def set_scrollbar(self, frame_margin=50, width=10, color=LIGHT_BLUE, alpha=150):
        ratio = float(self.text_screen_height) / self.text_surface.get_height()
        self.scrollbar = pygame.Rect(self.text_surface_position[0] + self.text_surface.get_width() + 2*self.margin - width, self.text_surface_position[1], width, self.text_screen_height*ratio)
        self.scrollbar = scrollbar(self.scrollbar, ratio, color)
    
    def set_surface(self, text, text_color, font1, margin, inner_margin):
        screen_width = self.screen.get_rect().width - (2*margin + 2*inner_margin)
        if len(text) >= 2048:
            temp_text = text
            title_width = 0
            while len(temp_text) > 2000:
                new_surface = font1.render(temp_text[:2000], 1, text_color)
                title_width += new_surface.get_rect().width
                temp_text = temp_text[2000:]
            new_surface = font1.render(temp_text, 1, text_color)
            title_width += new_surface.get_rect().width
        else:
            new_surface = font1.render(text, 1, text_color)
            title_width = new_surface.get_rect().width
        width_precentage = float(screen_width) / title_width
        title_lenght = len(text)
        line_surface = []
        while title_width > screen_width:
            pointer = int(title_lenght*width_precentage)
            new_title = text[:pointer]
            new_title = new_title.split(" ")
            if len(new_title) is not 1:
                pointer = pointer - len(new_title.pop(len(new_title) - 1))
            new_title = " ".join(word for word in new_title)
            if len(new_title) == 0:
                break
            new_title = font1.render(new_title, 1, text_color)
            line_surface.append(new_title)
            text = text[pointer:]
            title_width -= new_title.get_rect().width
        if text:# or self.is_scrollbar:
            line_surface.append(font1.render(text, 1, text_color))
        new_surface_height = sum([surface.get_rect().height for surface in line_surface])
        new_surface = pygame.Surface((screen_width, new_surface_height), pygame.SRCALPHA)
        new_surface.fill((255,255,255,0))
        new_surface_height = 0
        for line in line_surface:
            new_surface.blit(line, (0,new_surface_height))
            new_surface_height += line.get_rect().height
        return new_surface
    
    def set_title_surface(self, outer_margin):
        text_height = self.title_surface.get_rect().height
        text_width = self.title_surface.get_rect().width
        
        screen_height = self.screen.get_rect().height
        screen_width = self.screen.get_rect().width
        
        self.text_screen_height = self.text_surface.get_height()
        if self.text_surface.get_height() > screen_height - 2*outer_margin - 4*self.margin - self.title_surface.get_height():
            self.is_scrollbar = True
            temp_text_surface = self.text_surface
            self.text_screen_height = screen_height - 2*outer_margin - 2*self.margin - self.title_surface.get_height()
            self.text_surface = pygame.Surface((self.text_surface.get_width(),self.text_screen_height)) 
        
        X = 0.5*(screen_width - text_width) - 2*self.margin
        Y = self.title_surface_position[1] - self.margin
        rect = (X + 2*self.margin, Y, text_width + 2*self.margin, 0.5*(text_height + 2*self.margin))
        rect2 = (X, Y + 0.5*(text_height + 2*self.margin), text_width + 4*self.margin, 0.5*(text_height + 2*self.margin))
        rect3 = (X, Y + (text_height + 2*self.margin), self.margin, 2*self.margin + self.text_surface.get_rect().height)
        rect4 = (X, Y + text_height + 4*self.margin + self.text_surface.get_rect().height, text_width + 4*self.margin, self.margin)
        rect5 = (X + text_width + 3*self.margin, Y + (text_height + 2*self.margin), self.margin, 2*self.margin + self.text_surface.get_rect().height)
        
        points = []
        points.append((X + 2*self.margin, Y + 0.5*(text_height + 2*self.margin)))
        points.append((X + 2*self.margin, Y))
        points.append((X, Y + 0.5*(text_height + 2*self.margin)))
        color = (self.frame_window_color[0], self.frame_window_color[1], self.frame_window_color[2], self.title_surface_alpha)
        
        new_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        new_screen.fill((255,255,255,0))
        
        pygame.draw.rect(new_screen, color, rect, 0)
        pygame.draw.rect(new_screen, color, rect2, 0)
        pygame.draw.polygon(new_screen, color, points, 0)
        pygame.draw.rect(new_screen, color, rect3, 0)
        pygame.draw.rect(new_screen, color, rect4, 0)
        pygame.draw.rect(new_screen, color, rect5, 0)
        
        points.pop(0)
        points.append((X, rect3[1] + rect3[3] + rect4[3]))
        points.append((X + rect4[2], rect4[1] + rect4[3]))
        points.append((X + rect4[2], Y))
        pygame.draw.polygon(new_screen, self.frame_window_color, points, 1)
        
        new_screen.blit(self.title_surface, (self.title_surface_position[0], self.title_surface_position[1]))
        self.title_surface = new_screen
        if not self.text_screen_height == self.text_surface.get_height():
            self.text_surface = temp_text_surface
        else:
            self.text_screen_height += 2*self.margin
        
    def set_text_surface(self):
        if self.is_scrollbar:
            pass
    
    def draw_text_surface(self):
        text_height = self.text_surface.get_rect().height
        text_width = self.text_surface.get_rect().width
        
        screen_height = self.screen.get_rect().height
        screen_width = self.screen.get_rect().width
        
        X = 0.5*(screen_width - text_width) - 2*self.margin
        Y = self.text_surface_position[1] - self.margin
        new_screen = pygame.Surface((text_width + 2*self.margin, self.text_screen_height), pygame.SRCALPHA)
        if self.is_scrollbar:
            new_screen = pygame.Surface((text_width + 4*self.margin, self.text_screen_height), pygame.SRCALPHA)
            X -= self.margin
        new_screen.fill((self.window_color[0], self.window_color[1], self.window_color[2], self.text_surface_alpha))
        
        if self.is_scrollbar:
            new_screen.blit(self.text_surface, (self.margin, self.margin - 2*(self.scrollbar.scrollbar.top / self.scrollbar.ratio)))
        else:
            new_screen.blit(self.text_surface, (2*self.margin, self.margin))
        self.screen.blit(new_screen, (X + self.margin,Y))

    def draw_title_surface(self):
        self.screen.blit(self.title_surface, (0,0))
    
    def draw(self):
        self.draw_title_surface()
        self.draw_text_surface()
        if self.is_scrollbar:
            self.scrollbar.draw(self.screen)
    
    def draw_background(self, screen):
        """
        draws background on screen (does not update screen)
        """
        self.screen.blit(screen,(0,0))
    
    def run(self):
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if self.is_scrollbar:
                    if not self.scrollbar.scrolling_event(event):
                        return None
                    elif self.scrollbar.event(event, self.text_screen_height - 2*self.margin):
                        pass
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return None
            self.draw_background(self.background)
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
def main_button():
    button = retro_button("hello", (320, 240))
    button.run()

def main_window():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Game Menu')
    screen.fill(BLACK)
    for y in range(0,screen.get_rect().height, 4):
        pygame.draw.line(screen, RETRO_DARK_BLUE, (0,y), (screen.get_rect().width, y), 1)
    #title = "title"
    title = ""
    text = "Assigning to size, width or height changes the dimensions of the rectangle; all other assignments move the rectangle without resizing it. Notice that some attributes are integers and others are pairs of integers."
    text = text*15
    #text = ""
    print len(text)
    win = status_window(screen, title, text, text_color=WHITE)
    win.run()

if __name__ == "__main__":
    #scrollbar = scrollbar((0,0,0,0))
    #scrollbar.run()
    #main()
    main_window()
    #main_button()
    #time.sleep(10)
    pygame.quit()
