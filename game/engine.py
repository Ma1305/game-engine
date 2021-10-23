from managingFunctions import *
from graphics import *
from audio import *
from userKey import *

import pygame

gameGraphics.backgroundColor = (0,0,0)
gameGraphics.screenH = 600
gameGraphics.screenW = 800
gameGraphics.change_screen_dimensions(1400, 700)

buttonList = []
scroll_sensitivity = 7
going_down = True
going_up = True
buttonArea = pygame.Rect(0, 0, 150, screenH)


startB = Shape("start_button", None, 0, 0, 100, 100, (255, 255, 255), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*1, 100, 100, (100, 100, 100), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*2, 100, 100, (255, 255, 255), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*3, 100, 100, (100, 100, 100), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*4, 100, 100, (255, 255, 255), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*5, 100, 100, (100, 100, 100), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*6, 100, 100, (255, 255, 255), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*7, 100, 100, (100, 100, 100), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

startB = Shape("start_button", None, 0, 100*8, 100, 100, (255, 255, 255), gameGraphics.screen)
addShape(startB)
buttonList.append(startB)

button_scroll = Scrollable(buttonList, scroll_sensitivity, buttonArea, motion=10)
