import graphics
import manager
import shape_types
import copy
import user_input as ui
import random

BLOCK = 50
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PLAYER_RADIUS = BLOCK / 2 * 0.55
PLAYER_OPTIONS = []
PLAYER_DISTANCE = 5


last_game_code = 0

line_model = graphics.Shape(None, shape_types.line)
shape_types.change_to_line(line_model, (0, 0), (0, 0), (255, 255, 255))

manager.game_loop.make_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

for x in range(int((SCREEN_WIDTH*2/BLOCK-4)/PLAYER_DISTANCE)):
    for y in range(int((SCREEN_HEIGHT*2/BLOCK-4)/PLAYER_DISTANCE)):
        PLAYER_OPTIONS.append(((x+2+x*PLAYER_DISTANCE)*BLOCK, (y+2+y*PLAYER_DISTANCE)*BLOCK))



'''
vertical_lines = []
horizontal_lines = []


screen = graphics.Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
game_graphics = graphics.GameGraphics(screen, None)
camera = graphics.Camera(300, 200, 1, game_graphics)
game_graphics.camera = camera
graphics.add_game_graphics(game_graphics)

# set this game as main
manager.game_loop.make_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
manager.game_loop.set_main_game_graphics(game_graphics)

line_model = graphics.Shape(game_graphics, shape_types.line)
shape_types.change_to_line(line_model, (0, 0), (0, 0), (255, 255, 255))

for x in range(int(SCREEN_WIDTH/BLOCK*3)):
    line_model.game_graphics = None
    actual_line = copy.deepcopy(line_model)
    actual_line.start_point = (x * BLOCK, 0)
    actual_line.end_point = (x * BLOCK, SCREEN_HEIGHT*3)
    actual_line.game_graphics = game_graphics
    game_graphics.add_shape(actual_line)
    line_model.game_graphics = game_graphics
    horizontal_lines.append(actual_line)

for y in range(int(SCREEN_HEIGHT/BLOCK*3)):
    line_model.game_graphics = None
    actual_line = copy.deepcopy(line_model)
    actual_line.start_point = (0, y * BLOCK)
    actual_line.end_point = (SCREEN_WIDTH*3, y * BLOCK)
    actual_line.game_graphics = game_graphics
    game_graphics.add_shape(actual_line)
    line_model.game_graphics = game_graphics
    vertical_lines.append(actual_line)

print(len(horizontal_lines))
print(len(vertical_lines))

player = graphics.Shape(game_graphics, shape_types.circle)
shape_types.change_to_circle(player, (BLOCK/2 + SCREEN_WIDTH/2, BLOCK/2+SCREEN_HEIGHT/2), BLOCK/2*0.55, (255, 0, 0))


player_gun = graphics.Shape(game_graphics, shape_types.line)
shape_types.change_to_line(player_gun, player.center, (player.center[0], player.center[1]+BLOCK/2*0.9), (200, 0, 0), 7)
game_graphics.add_shape(player_gun)

game_graphics.add_shape(player)


def center_camera():
    camera.x = player.center[0]
    camera.y = player.center[1]


center_camera_looper = ui.Looper("center camera", center_camera)
game_graphics.add_looper(center_camera_looper)


def move_right():
    player.center = (player.center[0]+player_speed, player.center[1])


player_speed = 3
move_right_looper = ui.Looper("move right", move_right)
game_graphics.add_looper(move_right_looper)
'''


# converting a line shape object into a dictionary for networking purposes
def convert_line_to_dictionary(line):
    msg = {}
    msg["startpoint"] = line.start_point
    msg["endpoint"] = line.end_point
    msg["color"] = line.color
    return msg


# converting a player object into a dictionary for networking purposes
def convert_player_to_dictionary(player):
    msg = {}
    msg["pos"] = player.body.center
    msg["color"] = player.body.color
    msg["gun"] = {"shape": {"startpoint": player.gun.gun_shape.start_point, "endpoint": player.gun.gun_shape.end_point}}
    msg["code"] = player.client.code
    return msg


# creating a new game code
def get_game_code():
    global last_game_code
    last_game_code += 1
    return last_game_code


# checking for available game to join, if not it will create a new game
def get_available_game():
    for game_graphics in graphics.game_graphics_list:
        if len(game_graphics.storage["player_list"]) < game_graphics.storage["maximum"]:
            return game_graphics
    return create_game()


# crating a new player
def create_player(client):
    game_graphics = get_available_game()
    # creating a player's body and gun shapes
    random.shuffle(game_graphics.storage["available_positions"])
    pos = game_graphics.storage["available_positions"][0]
    game_graphics.storage["available_positions"].remove(pos)
    body = graphics.Shape(game_graphics, shape_types.circle)
    shape_types.change_to_circle(body, (pos[0] + BLOCK/2, pos[1] + BLOCK/2), PLAYER_RADIUS, (255, 0, 0))
    gun_shape = graphics.Shape(game_graphics, shape_types.line)
    shape_types.change_to_line(gun_shape, body.center, (body.center[0], body.center[1] + BLOCK / 2 * 0.9), (200, 0, 0), 7)
    game_graphics.add_shape(gun_shape)
    game_graphics.add_shape(body)

    # creating their actual object
    gun = Gun(gun_shape, None, game_graphics)
    player = Player(game_graphics, body, gun, client, pos)
    gun.player = player

    game_graphics.storage["player_list"].append(player)

    return player


# creating a new game
def create_game():
    global SCREEN_WIDTH, SCREEN_HEIGHT, line_model, PLAYER_OPTIONS

    # creating the new game_graphics
    screen = graphics.Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_graphics = graphics.GameGraphics(screen, None)
    camera = graphics.Camera(900, 600, 0.24, game_graphics)
    game_graphics.camera = camera
    graphics.add_game_graphics(game_graphics)

    # creating the background
    vertical_lines = []
    horizontal_lines = []

    for x in range(int(SCREEN_WIDTH / BLOCK * 2)):
        line_model.game_graphics = None
        actual_line = copy.deepcopy(line_model)
        actual_line.start_point = (x * BLOCK, 0)
        actual_line.end_point = (x * BLOCK, SCREEN_HEIGHT * 2)
        actual_line.game_graphics = game_graphics
        game_graphics.add_shape(actual_line)
        line_model.game_graphics = game_graphics
        horizontal_lines.append(actual_line)

    for y in range(int(SCREEN_HEIGHT / BLOCK * 2)):
        line_model.game_graphics = None
        actual_line = copy.deepcopy(line_model)
        actual_line.start_point = (0, y * BLOCK)
        actual_line.end_point = (SCREEN_WIDTH * 2, y * BLOCK)
        actual_line.game_graphics = game_graphics
        game_graphics.add_shape(actual_line)
        line_model.game_graphics = game_graphics
        vertical_lines.append(actual_line)

    # adding required variables
    game_graphics.storage["player_list"] = []
    game_graphics.storage["maximum"] = 3
    game_graphics.storage["vertical_lines"] = vertical_lines
    game_graphics.storage["horizontal_lines"] = horizontal_lines
    game_graphics.storage["game_code"] = get_game_code()
    game_graphics.storage["available_positions"] = PLAYER_OPTIONS.copy()
    game_graphics.storage["animation_list"] = []

    # set this game as main
    manager.game_loop.set_main_game_graphics(game_graphics)

    return game_graphics


class Player:
    def __init__(self, game_graphics, body, gun, client, pos):
        self.body = body
        self.gun = gun
        self.game_graphics = game_graphics
        self.client = client
        self.state = "stable"
        self.pos = pos

    def move(self, move):
        self.body.move(move)
        self.gun.move(move)

    def shoot(self, direction):
        self.gun.shoot(direction)

    def send(self, msg):
        self.client.send(msg)


class Gun:
    def __init__(self, gun_shape, player, game_graphics):
        self.gun_shape = gun_shape
        self.player = player
        self.game_graphics = game_graphics
        self.bullet_list = []

    def shoot(self, direction):
        pass

    def move(self, move):
        self.gun_shape.move(move)


class Bullet:
    def __init__(self, game_graphics, bullet_shape, gun, direction, speed):
        self.game_graphics = game_graphics
        self.bullet_shape = bullet_shape
        self.gun = gun
        self.direction = direction
        self.speed = speed

    def move(self, move):
        self.bullet_shape.move(move)

    def moving_bullet(self):
        pass


class MovingRightAnimation:
    def __init__(self, player, speed, block):
        self.player = player
        self.initial_speed = speed
        self.speed = speed
        self.block = block
        self.where = 0
        self.stage = 1
        self.animate_looper = None

    def animate(self):
        if self.where > (2*self.block)/3:
            self.stage = 2

        if self.stage == 1:
            self.speed += 0.04
        elif self.stage == 2:
            self.speed -= 0.04
        self.player.move((self.speed, 0))
        self.where += self.speed

        if self.where >= self.block:
            self.player.move((self.block - self.where, 0))

            if self.player.state != "move right":
                self.player.game_graphics.looper_list.remove(self.animate_looper)
                if self.player.state == "move left":
                    new_animation = MovingLeftAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move up":
                    new_animation = MovingUpAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move down":
                    new_animation = MovingDownAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
            else:
                self.stage = 1
                self.speed = self.initial_speed
                self.where = 0


class MovingLeftAnimation:
    def __init__(self, player, speed, block):
        self.player = player
        self.initial_speed = speed
        self.speed = speed
        self.block = block
        self.where = 0
        self.stage = 1
        self.animate_looper = None

    def animate(self):
        if self.where > 2*self.block/3:
            self.stage = 2

        if self.stage == 1:
            self.speed += 0.04
        elif self.stage == 2:
            self.speed -= 0.04
        self.player.move((-self.speed, 0))
        self.where += self.speed

        if self.where >= self.block:
            self.player.move((-(self.block - self.where), 0))

            if self.player.state != "move left":
                self.player.game_graphics.looper_list.remove(self.animate_looper)
                if self.player.state == "move right":
                    new_animation = MovingRightAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move up":
                    new_animation = MovingUpAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move down":
                    new_animation = MovingDownAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
            else:
                self.stage = 1
                self.speed = self.initial_speed
                self.where = 0


class MovingUpAnimation:
    def __init__(self, player, speed, block):
        self.player = player
        self.initial_speed = speed
        self.speed = speed
        self.block = block
        self.where = 0
        self.stage = 1
        self.animate_looper = None

    def animate(self):
        if self.where > 2*self.block/3:
            self.stage = 2

        if self.stage == 1:
            self.speed += 0.04
        elif self.stage == 2:
            self.speed -= 0.04
        self.player.move((0, self.speed))
        self.where += self.speed

        if self.where >= self.block:
            self.player.move((0, self.block - self.where))

            if self.player.state != "move up":
                self.player.game_graphics.looper_list.remove(self.animate_looper)
                if self.player.state == "move left":
                    new_animation = MovingLeftAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move right":
                    new_animation = MovingRightAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move down":
                    new_animation = MovingDownAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
            else:
                self.stage = 1
                self.speed = self.initial_speed
                self.where = 0


class MovingDownAnimation:
    def __init__(self, player, speed, block):
        self.player = player
        self.initial_speed = speed
        self.speed = speed
        self.block = block
        self.where = 0
        self.stage = 1
        self.animate_looper = None

    def animate(self):
        if self.where > 2*self.block/3:
            self.stage = 2

        if self.stage == 1:
            self.speed += 0.04
        elif self.stage == 2:
            self.speed -= 0.04
        self.player.move((0, -self.speed))
        self.where += self.speed

        if self.where >= self.block:
            self.player.move((0, -(self.block - self.where)))

            if self.player.state != "move down":
                self.player.game_graphics.looper_list.remove(self.animate_looper)
                if self.player.state == "move left":
                    new_animation = MovingLeftAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move up":
                    new_animation = MovingUpAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
                elif self.player.state == "move right":
                    new_animation = MovingRightAnimation(self.player, self.initial_speed, self.block)
                    new_animation_looper = ui.Looper("animation looper", new_animation.animate)
                    new_animation.animate_looper = new_animation_looper
                    self.player.game_graphics.add_looper(new_animation_looper)
            else:
                self.stage = 1
                self.speed = self.initial_speed
                self.where = 0


def get_player_animation(player, animation_list):
    for animation in animation_list:
        if animation.player == player:
            return animation
    return False


def convert_animation_to_dictionary(animation):
    message = {}

    message["speed"] = animation.speed
    message["where"] = animation.where
    message["stage"] = animation.stage

    return message
