from graphics import GameGraphics, Screen, Camera, add_game_graphics
from shapes import basics
import manager


# setup environment
screen = Screen(1000, 700)
camera = Camera(0, 0, 1, None)
game_env = GameGraphics(screen, camera)
camera.game_graphics = game_env
add_game_graphics(game_env)

manager.game_loop.set_main_game_graphics(game_env)
manager.game_loop.make_screen(1000, 700)


# setup some objects
square = basics.Square(game_env, (200, 200, 200), (0, 0, 100, 100))
game_env.add_shape(square)

circle = basics.Circle(game_env, (200, 200), 100, (255, 0, 0))
game_env.add_shape(circle)

line = basics.Line(game_env, (-50, -50), (-100, -100), (255, 255, 0), 3)
game_env.add_shape(line)
