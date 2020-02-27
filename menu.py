__author__ = "Mikey"

import pygame
from pygame import font, rect
from os.path import dirname, join
import status_window as Alert
import time
import re
import sys

pygame.init()
font.init()

GOLD = (229, 193, 0)
WHITE = (255,255,255)
RETRO_BLUE = (0,0,142)
BLACK = (0,0,0)
LIGHT_BLUE = (47,180,219)
RETRO_DARK_BLUE = (13,107,135)

class TextBox():
    def __init__(self, TB_max=20, fps_rate=60):
        self.pointer = 0
        self.textBox = ""
        self.max_character = TB_max
        self.fps = fps_rate
        if self.fps > 50:
            self.fps = 50
        self.on_screen = 0
    
    def get_text_Box_input(self):
        return self.textBox
    
    def set_text_Box_input(self, text):
        self.textBox = text
    
    def set_textbox_max_lenght(self, TB_max):
        self.max_character = TB_max
    
    def set_fps_rate(self, fps):
        self.fps = fps
    
    def marker_animation(self, screen, font, color, (x, y)):
        """
        draw animated pointer on screen.
        start position of textbox is (x,y)
        """
        if self.on_screen > (self.fps/2):
            label = font.render(self.textBox[:self.pointer], 1, color)
            x += label.get_width()
            label = font.render("|", 1, color)
            screen.blit(label, (x - 5, y))
            del label
        self.on_screen += 1
        self.on_screen %= self.fps
    
    def key_events(self, event):
        if event.key == pygame.K_LEFT:
            self.pointer -= 1
        elif event.key == pygame.K_RIGHT:
            self.pointer += 1
        elif event.key == pygame.K_BACKSPACE:
            if self.pointer == 0:
                pass
            elif self.pointer == len(self.textBox):
                self.textBox = self.textBox[:-1]
            else:
                self.textBox = self.textBox[:self.pointer - 1] + self.textBox[self.pointer:]
            self.pointer -= 1
        elif event.key == pygame.K_DELETE:
            if self.pointer == 0:
                self.textBox = self.textBox[1:]
            elif self.pointer == len(self.textBox):
                pass
            else:
                self.textBox = self.textBox[:self.pointer] + self.textBox[self.pointer + 1:]
        elif event.key == pygame.K_ESCAPE:
            return self.get_text_Box_input()
        elif len(self.textBox) == self.max_character:
            pass
        else:
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                return
            char = event.unicode
            if re.match("[\w-]", char):
                if self.pointer == 0:
                    self.textBox = char + self.textBox
                elif self.pointer == len(self.textBox):
                    self.textBox += char
                else:
                    self.textBox = self.textBox[:self.pointer] + char + self.textBox[self.pointer:]
                self.pointer += 1
        if self.pointer < 0:
            self.pointer = 0
        elif self.pointer > len(self.textBox):
            self.pointer = len(self.textBox)
    
    def run(self, screen, (x,y)):#does not work. missing functions
        clock = pygame.time.Clock()
        while 1:
            self.draw_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if self.key_events(event):
                        return None
            self.draw_password_text((x,y))
            self.marker_animation((x,y))
            pygame.display.flip()
            clock.tick(self.fps)

class menu_item():
    def __init__(self, name="",pos_X=0,pos_Y=0,item_width=0,item_height=0, type1="button", properties=None):
        self.name = name
        self.X = pos_X
        self.Y = pos_Y
        self.width = item_width
        self.height = item_height
        
        #advance options
        self.set_type(type1, properties)
    
    def set_type(self, type1, properties):
        """
        advance_options
        types include button, option, text, password
        """
        self.type1 = type1
        if self.type1 == "options":
            self.options = properties
            self.pointer = 0
        elif self.type1 == "text" or self.type1 == "password":
            self.text_box = TextBox(properties)
            self.start_tb_pos = (0, 0)
    
    def set_text_box(self, TB_max=20, fps_rate=60):
        try:
            self.text_box.set_textbox_max_lenght(TB_max)
            self.text_box.set_fps_rate(fps_rate)
        except:
            pass
    
    def set_options(self, options):
        try:
            self.options = options
            self.pointer = 0
        except:
            pass
    
    def set_pos(self, new_pos):
        self.X = new_pos[0]
        self.Y = new_pos[1]
        try:
            self.start_tb_pos = (0,0)
        except:
            pass
    
    def to_string(self):
        str1 = self.name + " is type '" + self.type1 + "'"
        str1 += "\n"
        str1 += "its position is (" + str(self.X) + ", " + str(self.Y) + ")"
        str1 += ", height=" + str(self.height) + " and width=" + str(self.width)
        return str1
    
    def draw_button(self, screen, font_obj, font_color):
        """
        draw menu text button on screen
        """
        label = font_obj.render(self.name, 1, font_color)
        screen.blit(label, (self.X, self.Y))
        
        #self.draw_arrows(screen, font_color)
    
    def draw_option_button(self, screen, font_obj, font_color):
        """
        get menu options button and draw it on screen
        """
        if self.type1 is not "options":
            return None
        
        label = font_obj.render(self.name + ": " + self.options[self.pointer], 1, font_color)
        screen.blit(label, (self.X, self.Y))
        
        self.draw_arrows(screen, font_color)
    
    def draw_input(self, screen, font_obj, font_color):
        """
        get menu input item and draw it on screen
        """
        if self.type1 is not "password" and self.type1 is not "text":
            return None
        
        if self.start_tb_pos == (0,0):
            label = font_obj.render(self.name + ": <", 1, font_color)
            label_width = label.get_rect().width
            self.start_tb_pos = (self.X + label_width, self.Y)
        if self.text_box.get_text_Box_input():
            if self.type1 == "password":
                label = font_obj.render(self.name + ": <", 1, font_color)
                label2 = font_obj.render("*"*len(self.text_box.get_text_Box_input()), 1, font_color)
                screen.blit(label2, (self.start_tb_pos[0], self.Y + 3))
                label3 = font_obj.render(">", 1, font_color)
                screen.blit(label3, (self.start_tb_pos[0] + label2.get_rect().width + 1, self.Y))
            else:
                label = font_obj.render(self.name + ": <" + self.text_box.get_text_Box_input() + ">", 1, font_color)
        else:
            label = font_obj.render(self.name + ": <enter "+ self.name + ">", 1, font_color)
        
        screen.blit(label, (self.X, self.Y))
        #self.draw_arrows(screen, font_color)
    
    def draw_arrows(self, screen, font_color):
        """
        draw option arrows
        """
        x,y = self.X, self.Y
        height = self.height - 6
        font_width = self.width
        tri_len = 12
        margin = 10
        x -= (margin + tri_len)
        y += 3
        
        pygame.draw.polygon(screen, font_color, ((x + tri_len, y), (x, y + height/2), (x + tri_len, y + height)))
        pygame.draw.polygon(screen, font_color, ((x + margin*2 + tri_len + font_width, y), (x + margin*2 + tri_len*2 + font_width, y + height/2), (x + margin*2 + tri_len + font_width, y + height)))
    
    def draw_item(self, screen, font_obj, font_color):
        """
        draw menu text button on screen
        """
        if self.type1 is "button":
            self.draw_button(screen, font_obj, font_color)
        elif self.type1 is "options":
            self.draw_option_button(screen, font_obj, font_color)
        else:
            self.draw_input(screen, font_obj, font_color)
    
    def change_menu_item_value(self, font_obj, properties=0):
        """
        update option selected in item or textbox_lenght and item new position, and size
        if item type is options, then properties is the change in pointer value (-1,0,1)
        if item type has textbox, the properties is None
        update and return self.width and self.height properties
        """
        if self.type1 is "options":
            self.pointer = (self.pointer + properties)%len(self.options)
            label = font_obj.render(self.name + ": " + self.options[self.pointer],1,BLACK)
        elif self.type1 is "button":
            return None
        else:
            if self.text_box.get_text_Box_input():
                label = font_obj.render(self.name + ": <" + self.text_box.get_text_Box_input() + ">", 1, BLACK)
            else:
                label = font_obj.render(self.name + ": <enter "+ self.name + ">", 1, BLACK)
        
        self.width = label.get_rect().width
        self.height = label.get_rect().height
        return self.width, self.height
    
    def option_arrows_is_pressed(self,mouse, menu, screen_width):
        """
        mouse - tuple holding mouse position
        menu - list of menu_item obj
        return position in menu and wheter left or right arrow is pressed
        if none then returns None
        """
        right_arrow = []
        left_arrow = []
        tri_len = 12
        margin = 10
        for item in menu:
            if item.type1 is not "options":
                continue
            x,y = item.X, item.Y
            height = item.height - 6
            font_width = item.width
            x -= (margin + tri_len)
            y += 3
            
            left_arrow.append(((x + tri_len, y), (x, y + height/2), (x + tri_len, y + height)))
            right_arrow.append(((x + margin*2 + tri_len + font_width, y), (x + margin*2 + tri_len*2 + font_width, y + height/2), (x + margin*2 + tri_len + font_width, y + height)))
        
        count = 0
        if mouse[0] > screen_width/2:
            for obj in right_arrow:
                rect = pygame.Rect((obj[0][0],obj[0][1], obj[1][0]-obj[0][0], obj[2][1] - obj[0][1]))
                if rect.collidepoint(mouse):
                    count2 = 0
                    for i in range(len(menu)):
                        if menu[i].type1 is "options":
                            if count == count2:
                                return (i, 1)
                            count2 += 1
                count += 1
        else:
            for obj in left_arrow:
                rect = pygame.Rect((obj[1][0],obj[0][1], obj[0][0]-obj[1][0], obj[2][1] - obj[0][1]))
                if rect.collidepoint(mouse):
                    count2 = 0
                    for i in range(len(menu)):
                        if menu[i].type1 is "options":
                            if count == count2:
                                return (i, -1)
                            count2 += 1
                count += 1
        
class Menu():
    def __init__(self, screen, menu, title, menu_font='FreePixel.ttf', menu_font_size=25, title_font='Cube.ttf', title_font_size=18, title_font_color=LIGHT_BLUE, font_color=LIGHT_BLUE, hover_color=WHITE):
        path = dirname(__file__)
        self.screen = screen
        self.width = self.screen.get_rect().width
        self.height = self.screen.get_rect().height
        
        #background
        self.bg_image = pygame.image.load(join(path,"corner-shadow1.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))
        
        #font and font color properties
        self.title_font = font.Font(join(path,title_font), title_font_size)
        self.menu_font = font.Font(join(path,menu_font),menu_font_size)
        self.menu_font_color = font_color
        self.menu_hover_font_color = hover_color
        self.title_font_color = title_font_color
        
        # menu properties
        self.item_spacing = 20
        self.title = title
        self.menu = menu
        
        self.hover_item = 0
    
    def draw_background(self):
        """
        draws background on screen (does not update screen)
        """
        self.screen.fill(BLACK)
        for y in range(0,self.height, 4):
            pygame.draw.line(self.screen, RETRO_DARK_BLUE, (0,y), (self.width, y), 1)
        self.screen.blit(self.bg_image,self.bg_image.get_rect(center=self.screen.get_rect().center))
    
    def draw_hover(self, item):
        """highlight item in hover_color and with a triangle arrow"""
        item.draw_item(self.screen, self.menu_font, self.menu_hover_font_color)
    
    def create_menu(self, title, items):
        """
        list of menu_item objs
        type = BUTTON
        title obj - list of titlename, width, height, pos_x, pos_y
        """
        menu = []
        ttl_height = 0
        
        label = self.title_font.render(title,1,self.title_font_color)
        label_width = label.get_rect().width
        label_height = label.get_rect().height
        pos_X = (self.width / 2) - (label_width / 2)
        menu.append([title, label_width, label_height, pos_X])
        ttl_height += label_height
        ttl_height += self.item_spacing*2
        for item in items:
            label = self.menu_font.render(item,1,self.menu_font_color)
            label_width = label.get_rect().width
            label_height = label.get_rect().height
            pos_X = (self.width / 2) - (label_width / 2)
            menu_item_obj = menu_item(item, pos_X, 0, label_width, label_height, "button")
            menu.append(menu_item_obj)
            ttl_height += label_height
        pos_Y = (self.height - (ttl_height + self.item_spacing*(len(items) -1)))/2
        title = menu.pop(0)
        title.append(pos_Y - self.item_spacing*2)
        pos_Y += self.item_spacing*2
        for item in menu:
            item.set_pos((item.X, pos_Y))
            pos_Y += item.height + self.item_spacing
        return title, menu
    
    def print_menu(self, menu):
        print "\n".join(str(item) for item in menu)
    
    def draw_title(self):
        """
        draw the title obj on the screen
        """
        label = self.title_font.render(self.title[0], 1, self.title_font_color)
        self.screen.blit(label, (self.title[3], self.title[4]))
    
    def draw_menu(self):
        """
        draw menu on screen
        """
        self.draw_title()
        for item in self.menu:
            item.draw_item(self.screen, self.menu_font, self.menu_font_color)
    
    def hover(self, mouse):
        #crush
        """
        check if mouse is on one of the menu items
        returns pos in menu list[ - int] and update selected item
        """
        count = 0
        for item in self.menu:
            rect = pygame.Rect((item.X, item.Y, item.width, item.height))
            if rect.collidepoint(mouse):
                self.hover_item = count
                return count
            count += 1
        return None
    
    def run(self):
        """
        run basic menu
        returns button name when pressed
        """
        if type(self.title) == type("string"):
            self.title, self.menu = self.create_menu(self.title, self.menu)
        clock = pygame.time.Clock()
        while 1:
            self.draw_background()
            self.draw_menu()
            
            obj = self.hover(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if type(obj) == type(1):
                        return self.menu[obj].name
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return self.menu[self.hover_item].name
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.hover_item -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.hover_item += 1
                    self.hover_item %= len(self.menu)
            
            self.draw_hover(self.menu[self.hover_item])
            pygame.display.flip()
            clock.tick(60)

class AdvanceMenu(Menu):
    """
    adds type - 
        1/opt-button
        2/button
        2/password-input
        3/text-input
    menu - list of [item name, type, [options(str)] or max_character(int)]
    """
    def create_menu(self, title, items):
        """
        list of menu_item objs
        type = 
            1/options
            2/password
            3/text
            4/button
        title obj - list of titlename, width, height, pos_x, pos_y
        """
        menu, temp_menu = [],[]
        for item in self.menu:
            menu.append(item[0])
            temp_menu.append([item[1],item[2]])
        title, menu = Menu.create_menu(self, title, menu)
        for i in range(len(menu)):
            menu[i].set_type(temp_menu[i][0], temp_menu[i][1])
            if menu[i].type1 is "button":
                continue
            menu_width, menu_height = menu[i].change_menu_item_value(self.menu_font)
            menu[i].set_pos(((self.width - menu_width)/2, menu[i].Y))
        return title, menu

    def menu_values(self):
        dict = {}
        for item in self.menu:
            if item.type1 is "options":
                dict[item.name] = item.options[item.pointer]
            elif item.type1 is "button":
                pass
            else:
                dict[item.name] = item.text_box.get_text_Box_input()
        return dict
    
    def draw_hover(self, item):
        """
        highlight item in hover_color and with a triangle arrow
        if hover item is a textbox add marker animation
        """
        if item.type1 == "text" or item.type1 == "password":
            item.text_box.marker_animation(self.screen, self.menu_font, self.menu_hover_font_color, item.start_tb_pos)
        item.draw_item(self.screen, self.menu_font, self.menu_hover_font_color)
    
    def options_type_keyboard_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            menu_width, menu_height = self.menu[self.hover_item].change_menu_item_value(self.menu_font, -1)
            self.menu[self.hover_item].set_pos(((self.width - menu_width)/2, self.menu[self.hover_item].Y))
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            menu_width, menu_height = self.menu[self.hover_item].change_menu_item_value(self.menu_font, 1)
            self.menu[self.hover_item].set_pos(((self.width - menu_width)/2, self.menu[self.hover_item].Y))
        else:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.hover_item -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.hover_item += 1
    
    def button_type_keyboard_events(self, event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            return self.menu[self.hover_item].name
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.hover_item -= 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.hover_item += 1
    
    def input_type_keyboard_events(self, event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.hover_item += 1
        elif event.key == pygame.K_UP:
            self.hover_item -= 1
        elif event.key == pygame.K_DOWN:
            self.hover_item += 1
        else:
            return self.menu[self.hover_item].text_box.key_events(event)
    
    def run(self):
        """
        run basic menu
        returns button name when pressed
        returns menu_values when esc button is pressed
        """
        if type(self.title) == type("string"):
            self.title, self.menu = self.create_menu(self.title, self.menu)
        clock = pygame.time.Clock()
        while 1:
            self.draw_background()
            self.draw_menu()
            obj = self.hover(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu[self.hover_item].type1 is "button":
                        if type(obj) == type(1):
                            return self.menu[obj].name
                    obj = self.menu[0].option_arrows_is_pressed(pygame.mouse.get_pos(), self.menu, self.width)
                    if obj:
                        self.hover_item = obj[0]
                        menu_width, menu_height = self.menu[self.hover_item].change_menu_item_value(self.menu_font, obj[1])
                        self.menu[self.hover_item].set_pos(((self.width - menu_width)/2, self.menu[self.hover_item].Y))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.menu_values()
                    elif self.menu[self.hover_item].type1 is "options":
                        self.options_type_keyboard_events(event)
                    elif self.menu[self.hover_item].type1 is "button":
                        obj = self.button_type_keyboard_events(event)
                        if obj:
                            return obj
                    else:
                        obj = self.input_type_keyboard_events(event)
                        if obj:
                            return obj
                        else:
                            if self.menu[self.hover_item].type1 is "text" or self.menu[self.hover_item].type1 is "password":
                                menu_width, menu_height = self.menu[self.hover_item].change_menu_item_value(self.menu_font)
                                self.menu[self.hover_item].set_pos(((self.width - menu_width)/2, self.menu[self.hover_item].Y))
                    self.hover_item %= len(self.menu)
            
            self.draw_hover(self.menu[self.hover_item])
            pygame.display.flip()
            clock.tick(60)

class Form_Menu(AdvanceMenu):
    def __init__(self, form_type, screen, menu, title, menu_font='FreePixel.ttf', menu_font_size=25, title_font='Cube.ttf', title_font_size=18, title_font_color=LIGHT_BLUE, font_color=LIGHT_BLUE, hover_color=WHITE):
        AdvanceMenu.__init__(self, screen, menu, title, menu_font, menu_font_size, title_font, title_font_size, title_font_color, font_color, hover_color)
        self.form_type = form_type
    
    def validate_form_login(self, form_dict):
        try:
            if form_dict["Password"] == form_dict["Password2"]:
                return form_dict
            else:
                Alert = PopUpAlert(self.screen)
                Alert.run("QUESTION", "passwords do not match")
        except:
            alert = Alert.status_window(self.screen, "", "Game menu Error: missing values")
            alert.run()
            return -1
    
    def validate_form_register(self, form_dict):
        try:
            for item in self.menu:
                if item.type1 is not "button":
                    if not form_dict[item.name]:
                        alert = Alert.status_window(self.screen, "", item.name + " is empty")
                        alert.run()
                        return None
            return form_dict
        except:
            alert = Alert.status_window(self.screen, "", "Game menu Error: missing values")
            alert.run()
            return -1
    
    def run(self):
        val = AdvanceMenu.run(self)
        if val == "reset":
            for item in self.menu:
                if item.type1 == "options":
                    item.pointer = 0
                elif item.type1 == "button":
                    pass
                else:
                    item.text_box.set_text_Box_input("")
                    menu_width, menu_height = item.change_menu_item_value(self.menu_font)
                    item.set_pos(((self.width - menu_width)/2, item.Y))
            return self.run()
        elif val == "submit":
            if self.form_type == "register":
                obj = self.validate_form_register(self.menu_values())
                if obj:
                    if type(obj) == type(1):
                        alert = Alert.status_window(self.screen, "NOTE", "please change or override validate_form_register function")
                        alert.run()
                        return -1
                    return obj
                return self.run()
            elif self.form_type == "login":
                obj = self.validate_form_login(self.menu_values())
                if obj:
                    if type(obj) == type(1):
                        alert = Alert.status_window(self.screen, "NOTE", "please change or override validate_form_register function")
                        alert.run()
                        return -1
                    return obj
                return self.run()
            else:
                alert = Alert.status_window(self.screen, "ERROR", "please add " + self.form_type + " validate_form_function and override/(add if to) run function")
                alert.run()
                return -1
        elif val == "exit":
            return val
        else:
            alert = Alert.status_window(self.screen, "NOTE", "user used esc button to leave")
            alert.run()
            return val
    
def BasicMenu_check(screen):
    menu = [
            "log in",
            "register",
            "log out",
            "setting",
            "quit"
            ]
    title = "the resistance"
    game_menu = Menu(screen, menu, title)
    return game_menu.run()

def AdvanceMenu_check(screen):
    menu = [["username","text", 20],
            ["password","password", 20],
            ["reset", "button", None],
            ["num of players", "options", ["5","6", "7","8","9","10"]]
            ]
    title = "the resistance"
    game_menu = AdvanceMenu(screen, menu, title)
    return game_menu.run()

def Form_Menu_check(screen):
    menu = [["username","text", 20],
            ["password","password", 20],
            ["reset", "button", None],
            ["submit", "button", None],
            ["num of players", "options", ["5","6", "7","8","9","10"]]
            ]
    title = "the resistance"
    game_menu = Form_Menu("register", screen, menu, title)
    return game_menu.run()

def terminate():
    print "2"
    pygame.quit()
    sys.exit()

def __del__(self):
    print "1"
    del screen
    terminate()
    
if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
    #screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    pygame.display.set_caption('Game Menu')
    screen.fill((255,255,255))
    print Form_Menu_check(screen)
    #time.sleep(10)
    pygame.quit()