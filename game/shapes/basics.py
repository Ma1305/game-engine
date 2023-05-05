import graphics
import pygame
import math


class Square(graphics.Shape):
    def __init__(self, game_graphics, color, rect, real=False):
        super().__init__(game_graphics, "SQUARE")
        self.color = color
        self.rect = rect
        self.real = real

    def draw(self):
        if self.real:
            pygame.draw.rect(self.game_graphics.screen.screen, self.color, self.rect)
            return None
        pos = self.game_graphics.camera.vr_to_real((self.rect[0], self.rect[1]))
        w = self.game_graphics.camera.zoom * self.rect[2]
        h = self.game_graphics.camera.zoom * self.rect[3]
        pygame.draw.rect(self.game_graphics.screen.screen, self.color, (pos[0], pos[1], w, h))

    def move(self, movement):
        self.rect = (self.rect[0] + movement[0], self.rect[1] + movement[1], self.rect[2], self.rect[3])


class Line(graphics.Shape):
    def __init__(self, game_graphics, start_point, end_point, color, width=1, real=False):
        super().__init__(game_graphics, "LINE")
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.width = width
        self.real = real

    def draw(self):
        if self.real:
            pygame.draw.line(self.game_graphics.screen.screen, self.color, self.start_point, self.end_point, self.width)
            return None
        start_point = self.game_graphics.camera.vr_to_real(self.start_point)
        end_point = self.game_graphics.camera.vr_to_real(self.end_point)
        width = math.ceil(self.game_graphics.camera.zoom * self.width)
        pygame.draw.line(self.game_graphics.screen.screen, self.color, start_point, end_point, width)

    def move(self, movement):
        self.start_point = (self.start_point[0] + movement[0], self.start_point[1] + movement[1])
        self.end_point = (self.end_point[0] + movement[0], self.end_point[1] + movement[1])


class Circle(graphics.Shape):
    def __init__(self, game_graphics, center, radius, color, real=False):
        super().__init__(game_graphics, "CIRCLE")
        self.center = center
        self.radius = radius
        self.color = color
        self.real = real

    def draw(self):
        if self.real:
            pygame.draw.circle(self.game_graphics.screen.screen, self.color, self.center, self.radius)
            return None
        center = self.game_graphics.camera.vr_to_real(self.center)
        radius = self.game_graphics.camera.zoom * self.radius
        pygame.draw.circle(self.game_graphics.screen.screen, self.color, center, radius)

    def move(self, movement):
        self.center = (self.center[0] + movement[0], self.center[1] + movement[1])
