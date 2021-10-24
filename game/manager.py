import pygame


class GameLoop:
    def __init__(self):
        self.fps = 50
        self.clock = None
        self.screen = None
        self.screen_width = None
        self.screen_height = None
        self.main_game_graphics = None

    def make_screen(self, width, height):
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((width, height))

    def set_main_game_graphics(self, game_graphics):
        self.main_game_graphics = game_graphics


game_loop = GameLoop()

