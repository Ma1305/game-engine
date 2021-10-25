import pygame
import graphics as graphics


def change_to_square(shape, color, rect, real=False):
    shape.color = color
    shape.rect = rect
    shape.real = real


def draw_square(self):
    if self.real:
        pygame.draw.rect(self.game_graphics.screen.screen, self.color, self.rect)
        return None
    pos = self.game_graphics.camera.vr_to_real((self.rect[0], self.rect[1]))
    w = self.game_graphics.camera.zoom*self.rect[2]
    h = self.game_graphics.camera.zoom*self.rect[3]
    pygame.draw.rect(self.game_graphics.screen.screen, self.color, (pos[0], pos[1], w, h))


square = graphics.Type("square", draw_square)
graphics.add_type(square)


def change_to_line(shape, start_point, end_point, color, width=1, real=False):
    shape.start_point = start_point
    shape.end_point = end_point
    shape.color = color
    shape.width = width
    shape.real = real

def draw_line(self):
    if self.real:
        pygame.draw.line(self.game_graphics.screen.screen, self.color, self.start_point, self.end_point, self.width)
        return None
    start_point = self.game_graphics.camera.vr_to_real(self.start_point)
    end_point = self.game_graphics.camera.vr_to_real(self.end_point)
    pygame.draw.line(self.game_graphics.screen.screen, self.color, start_point, end_point, self.width)


line = graphics.Type("line", draw_line)
graphics.add_type(line)
