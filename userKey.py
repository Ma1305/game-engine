import pygame
import threading


# game restart reset
funcList = []
def checkForFuncitons(event):
    for func in funcList:
        func(event)

# new function to be added to the list of triggers for the game loop
def newInFunc(OnEvent, action):
    global funcList
    def func(event):
        if event.type == OnEvent:
            action()

    funcList.append(func)


# new key function to be added to the list of triggers for the game loop
def newKeyFunc(onEvent, action):
    global funcList
    def func(event):


        while pygame.key.get_pressed()[onEvent]:
            action()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    break

    funcList.append(func)

# new if key function to be added to the list of triggers for the game loop
def newKeyIfFunc(onEvent, action):
    global funcList

    def func(event):

        if event.type == pygame.KEYDOWN:
            if event.key == onEvent:
                action()


    funcList.append(func)

# new if key function to be added to the list of triggers for the game loop
def newEventableFunc(onEvent, action):
    global funcList

    def func(event):

        if event.type == onEvent:
            action(event)


    funcList.append(func)



scroll = {
    "down": 4,
    "up": 5
}


