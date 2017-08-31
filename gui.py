#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
pygame.init() # Инициация PyGame, обязательная строчка 

from pygame import Surface, Color, sprite, QUIT, HWSURFACE, DOUBLEBUF, \
    FULLSCREEN
from config import *

class MenuResources(object):
    def __init__(self):
        super(MenuResources, self).__init__()
        self.buttons_dir = 'buttons/'

        save_button_images = ['0_save_game.png',
                        '1_save_game.png',
                        '2_save_game.png']
        self.save_button_images = self.load_button_images(save_button_images)

        new_game_images = ['0_new_game.png',
                        '1_new_game.png',
                        '2_new_game.png']
        self.new_game_button_images = self.load_button_images(new_game_images)

        exit_button_images = ['0_exit.png',
                        '1_exit.png',
                        '2_exit.png']
        self.exit_button_images = self.load_button_images(exit_button_images)

        settings_images = ['0_settings.png',
                        '1_settings.png',
                        '2_settings.png']
        self.settings_button_images = self.load_button_images(settings_images)
        

    def load_button_images(self, images):
        button_images = []
        for image in images:
            button_image = pygame.image.load(self.buttons_dir + image)
            button_image = button_image.convert_alpha()
            button_images.append(button_image)
        return button_images

class Menu(object):
    def __init__(self, window_resolution, menu_dimensions):
        super(Menu, self).__init__()
        self.window_resolution = window_resolution
        self.menu_dimensions = menu_dimensions
        self.buttons = []
        self.buttons_sprite_group = pygame.sprite.LayeredDirty()
        self.gap = 0.2

    def add_button(self, button):
        self.buttons.append(button)
        self.buttons_sprite_group.add(button)

    def balance_buttons(self):
        amount_buttons = len(self.buttons)
        if amount_buttons is not 0:
            the_scale = self.calculate_the_scale(amount_buttons)
            self.scale_buttons(the_scale)
            button_height = self.buttons[0].get_heigth()
            gap_between_button = button_height * self.gap

            top_pos = (self.window_resolution[1] - self.menu_dimensions[1])
            top_pos = top_pos / 2 + gap_between_button + button_height / 2

            for i, button in enumerate(self.buttons):
                new_y_pos = top_pos + i * (button_height + gap_between_button)
                button.set_y_pos(new_y_pos)

    def scale_buttons(self, the_scale):
        for button in self.buttons:
            button.scale(the_scale)

    def calculate_the_scale(self, amount_buttons):
        button_height = self.buttons[0].get_heigth()
        gap_between_button = button_height * self.gap
        buttons_height = amount_buttons * button_height
        gap_heigth = gap_between_button * (amount_buttons + 1)
        height = buttons_height + gap_heigth
        the_scale_height = self.menu_dimensions[1] / height

        button_width = self.buttons[0].get_width()
        the_scale_width = self.menu_dimensions[0] / button_height

        return min([the_scale_height, the_scale_width])

    def get_sprite_group(self):
        return self.buttons_sprite_group

    def render(self, screen):
        rects = self.buttons_sprite_group.draw(screen)
        pygame.display.update(rects)

    def сycle_of_work(self, screen, fps=30):
        timer = pygame.time.Clock()
        while True:
            timer.tick(fps)
            self.event_handler()
            self.render(screen)
            self.controller_handler()

    def event_handler(self):
        mouse_position = pygame.mouse.get_pos()
        active_button = get_active_button(mouse_position, 
                                          self.buttons_sprite_group)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit

            if e.type == pygame.MOUSEBUTTONDOWN:
                if active_button:
                    active_button.set_pressed()

            if e.type == pygame.MOUSEBUTTONUP:
                if active_button:
                    active_button.set_normal()

            if e.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    if button.is_pressed():
                        continue
                    if button is active_button:
                        button.set_active()
                    else:
                        button.set_normal()

    def controller_handler(self):
        for button in self.buttons:
            if button.is_pressed():
                button.run_controller()
        

class Button(pygame.sprite.DirtySprite):
    def __init__(self, position, images):
        sprite.DirtySprite.__init__(self)
        self.images = images
        self.set_normal()

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.controller = None

        self.dirty = 2
        #self.layer = 0
        #self.visible = 1
        #self.blendmode = 0
        #self.source_rect = None

    def set_normal(self):
        self.set_state(0)

    def set_active(self):
        self.set_state(1)

    def set_pressed(self):
        self.set_state(2)

    def set_state(self, new_state):
        self.state = new_state
        self.image = self.images[self.state]

    def set_x_pos(self, x):
        self.rect.center = x, self.rect.center[1]

    def set_y_pos(self, y):
        self.rect.center = self.rect.center[0], y

    def get_width(self):
        return self.rect.width

    def get_heigth(self):
        return self.rect.height

    def is_pressed(self):
        return self.state == 2

    def scale(self, the_scale):
        scaled_images = []
        for image in self.images:
            width, height = self.get_width(), self.get_heigth()
            new_dimensions = (int(width*the_scale), int(height*the_scale))
            img = pygame.transform.scale(image, new_dimensions)
            scaled_images.append(img)
        self.images = scaled_images
        self.apply_scaled_image()

    def apply_scaled_image(self):
        self.image = self.images[self.state]
        position = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = position

    def set_controller(self, function):
        self.controller = function

    def run_controller(self):
        if self.controller is not None:
            self.controller()

def get_active_button(cursor, gui_buttons):
    for button in gui_buttons:
        if button.rect.collidepoint(cursor):
            return button
    return None
        

def init_main_menu():
    resources = MenuResources()
    main_menu = Menu((WIN_WIDTH,WIN_HEIGHT), (300, 400))
    button_pos = (WIN_WIDTH/2, WIN_HEIGHT/2)
    new_game_button = Button(button_pos, resources.new_game_button_images)
    main_menu.add_button(new_game_button)
    settings_button = Button(button_pos, resources.settings_button_images)
    main_menu.add_button(settings_button)
    exit_button = Button(button_pos, resources.exit_button_images)
    def exit():
        raise SystemExit
    exit_button.set_controller(exit)
    main_menu.add_button(exit_button)
    main_menu.balance_buttons()
    return main_menu


def main():
    screen = pygame.display.set_mode(DISPLAY,  HWSURFACE|DOUBLEBUF|FULLSCREEN)
    screen.fill(Color(BACKGROUND_COLOR))
    pygame.display.set_caption("Gui")
    
    main_menu = init_main_menu()
    gui_buttons = main_menu.get_sprite_group()
       
    main_menu.сycle_of_work(screen)


if __name__ == "__main__":
    main()