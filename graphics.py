import pygame
pygame.init()

# storing game graphics information, only one available
class GameGraphics:
    def __init__(self, tfps, screenW, screenH, screen, backgroundColor):
        self.tfps = tfps
        self.screenW = screenW
        self.screenH = screenH
        self.screen = screen
        self.backgroundColor = backgroundColor
        self.videoBackground = False

    def change_screen_dimensions(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        screenW = width
        screenH = height



screenW = 500
screenH = 700
tfps = 55
backgroundColor = (100,0,0)
screen = pygame.display.set_mode((screenW, screenH))
frameCounter = 1

gameGraphics = GameGraphics(tfps, screenW, screenH, screen, backgroundColor)

# game restart reset
objects = []
triggerList = []


# a class that stores a shape information
class Shape:
    def __init__(self, name, py, x, y, w, h, color, screen):
        self.name = name
        self.py = py
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.screen = screen
        # second part of the list is the divisiblity frame
        self.xChange = [0, 1]
        self.yChange = [0, 1]
        self.colorChange = [(0, 0, 0), 1]
        self.wChange = [0, 1]
        self.hChange = [0, 1]
        self.animation = False
        self.posFraming = 0
        self.posFrameStart = 0
        self.animating = False
        self.animations = []
        self.customDraw = False
        self.customDrawFunc = None
        self.model = None
        self.state = True

    def draw(self):
        if self.state == True:
            if self.customDraw == True:
                self.customDrawFunc(self)
            else:
                self.py = pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.w, self.h))

    def addCustomDraw(self, newDrawFunc):
        self.customDraw = True
        self.customDrawFunc = newDrawFunc

    # add animation to the shape, there is a list of animation
    def addAnimation(self, animationList, animationRepeat, name, state):
        self.animating = True
        self.animations.append(Animation(animationList, animationRepeat, name, state))

    def startAnimation(self, name):
        for animation in self.animations:
            if animation.name == name:
                animation.state = True
        return False

    def getAnimationByName(self, name):
        for animation in self.animations:
            if animation.name == name:
                return animation
        return False

    def animationChanges(self):
        for animation in self.animations:
            if animation.state == True:
                animation.frame += 1
                #print(animation.animationList[animation.partOn])
                if animation.frame > animation.animationList[animation.partOn][4]:
                    animation.partOn += 1
                    animation.frame = 0
                if animation.partOn > animation.parts-1:
                    animation.partOn = 0
                    if animation.animationRepeat == False:
                        animation.state = False
                self.x += animation.animationList[animation.partOn][0]
                self.y += animation.animationList[animation.partOn][1]
                self.w += animation.animationList[animation.partOn][2]
                self.h += animation.animationList[animation.partOn][3]


    def change(self, frameCounter):
        if self.posFrameStart < self.posFraming:
            if frameCounter%self.xChange[1] == 0:
                self.x += self.xChange[0]
            if frameCounter%self.yChange[1] == 0:
                self.y += self.yChange[0]
            self.posFrameStart += 1
        if frameCounter%self.wChange[1] == 0:
            self.w += self.wChange[0]
        if frameCounter%self.hChange[1] == 0:
            self.h += self.hChange[0]

# a class that stores animation information
class Animation:
    def __init__(self, animationList, animationRepeat, name, state):
        self.animationList = animationList
        self.animationRepeat = animationRepeat
        self.name = name
        self.state = state
        self.frame = 0
        self.parts = len(animationList)
        self.partOn = 0


# a function that is gonna be run in fps
# it makes sure all the functions in it are gonna get run
def triggers():
    for trigger in triggerList:
        trigger()

# adding a function to be run in fps
def addTrigger(triggerFunc):
    global triggerList
    triggerList.append(triggerFunc)

# add a shape to shape list
def addShape(shape):
    global objects
    objects.append(shape)

# delete a shape from shape list
def deleteShapeByName(name):
    global objects
    for shape in objects:
        if shape.name == name:
            objects.remove(shape)


# make a new position movement
def changePos(shape, move, framing):
    shape.animation = True
    shape.xChange[0] = move[0]
    shape.yChange[0] = move[1]
    shape.posFraming = framing
    shape.posFrameStart = 0

# this will change all the things that has been set up to change
def doAChange():
    global objects
    for shape in objects:
        if shape.animation == True:
            shape.change(frameCounter)
        if shape.animating == True:
            shape.animationChanges()


# count frames, restarts the counter on target fps
# if fps is not the same as target fps this can be useful
def counterKeeper():
    global frameCounter
    frameCounter += 1
    if frameCounter >= tfps:
        frameCounter = 0


def drawBackground():
    if not gameGraphics.videoBackground:
        gameGraphics.screen.fill(gameGraphics.backgroundColor)

# draw the shapes to screen
def draw():
    global gameGraphics
    global objects
    doAChange()
    for thing in objects:
        thing.draw()



# update the screen
def updateS():

    pygame.display.update()




def changeToText(text, centerIt, background, backgroundColor, font, size, shape):
    shape.textContent = text
    shape.centerIt = centerIt
    shape.background = background
    shape.backgroundColor = backgroundColor
    shape.font = font
    shape.size = size
    def drawText(shape):
        font = pygame.font.Font(shape.font, shape.size)
        text = font.render(shape.textContent, shape.background, shape.color, shape.backgroundColor)
        textRect = text.get_rect()
        if shape.centerIt:
            textRect.center = (shape.x, shape.y)
        else:
            textRect.x = shape.x
            textRect.y = shape.y
        shape.screen.blit(text, textRect)
    shape.addCustomDraw(drawText)

# a function that turns the shape type into picture
def changeToPic(shape, fileName):
    shape.fileName = fileName
    shape.file = pygame.image.load(fileName)
    shape.model = "image"
    def imageDraw(shape):
        shape.py = shape.screen.blit(shape.file, (shape.x, shape.y))
    shape.addCustomDraw(imageDraw)

non_FPS_triggerList = []
def non_FPS_triggers():
    global non_FPS_triggerList
    for trigger in non_FPS_triggerList:
        trigger()

def add_non_fps_trigger(function):
    global non_FPS_triggerList
    non_FPS_triggerList.append(function)


