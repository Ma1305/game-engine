from game import graphics, manager
from game.shape_types import *
import pygame
import game.user_input as ui


# setting up a game_graphics
screen = graphics.Screen(1000, 700)
game_graphics = graphics.GameGraphics(screen, None)
camera = graphics.Camera(0, 0, 1, game_graphics)
game_graphics.camera = camera
graphics.add_game_graphics(game_graphics)


# setting up the screen and main graphics
manager.game_loop.make_screen(1000, 700)
manager.game_loop.set_main_game_graphics(game_graphics)


# creating squares
s1 = graphics.Shape(game_graphics, square)
change_to_square(s1, (255, 255, 255), (-25, 25, 50, 50))
game_graphics.add_shape(s1)

s2 = graphics.Shape(game_graphics, square)
change_to_square(s2, (255, 255, 255), (400, 100, 50, 50))
game_graphics.add_shape(s2)

# creating axis
y_axis = graphics.Shape(game_graphics, line)
change_to_line(y_axis, (0, -100000), (0, 100000), (163, 85, 39))
game_graphics.add_shape(y_axis)

x_axis = graphics.Shape(game_graphics, line)
change_to_line(x_axis, (-100000, 0), (100000, 0), (163, 85, 39))
game_graphics.add_shape(x_axis)


# moving screen with mouse
speed = 10
first_mouse_pos = (0, 0)
second_mouse_pos = (0, 0)
original_cam_pos = (0, 0)


def move_screen():
    global speed
    global camera
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        camera.move((speed, 0))
    if keys[pygame.K_LEFT]:
        camera.move((-speed, 0))
    if keys[pygame.K_UP]:
        camera.move((0, speed))
    if keys[pygame.K_DOWN]:
        camera.move((0, -speed))


def move_screen_with_mouse1():
    global first_mouse_pos, original_cam_pos
    first_mouse_pos = pygame.mouse.get_pos()
    original_cam_pos = (camera.x, camera.y)


def move_screen_mouse2():
    global first_mouse_pos, second_mouse_pos, original_cam_pos
    if pygame.mouse.get_pressed()[0]:
        second_mouse_pos = pygame.mouse.get_pos()
        camera.x = original_cam_pos[0] + -(second_mouse_pos[0] - first_mouse_pos[0]) / camera.zoom
        camera.y = original_cam_pos[1] + (second_mouse_pos[1] - first_mouse_pos[1]) / camera.zoom


move_screen_with_mouse1_input_func = ui.InputFunc("move screen with mouse 1", pygame.MOUSEBUTTONDOWN,
                                                  move_screen_with_mouse1)
move_screen_with_mouse2_looper = ui.Looper("move screen with mouse 2", move_screen_mouse2)

game_graphics.add_input_func(move_screen_with_mouse1_input_func)
game_graphics.add_looper(move_screen_with_mouse2_looper)

move_screen_looper = ui.Looper("move screen", move_screen)
game_graphics.add_looper(move_screen_looper)


# zooming
def zoom(event):
    global first_mouse_pos, second_mouse_pos
    if event.button == 4:
        camera.zoom /= 0.9
    elif event.button == 5:
        camera.zoom *= 0.9


zoom_input_func = ui.InputFunc("zoom", pygame.MOUSEBUTTONDOWN, zoom, pass_event=True)
game_graphics.add_input_func(zoom_input_func)



