import pygame
import managingFunctions
import userKey
import graphics
import audio
import videos
import pygame

run = True

# game loop where all the graphics are gonna get rendered and all triggers are gonna get executed

clock = pygame.time.Clock()
while run == True:
    graphics.triggers()
    graphics.drawBackground()
    videos.drawVideos()
    graphics.draw()
    graphics.updateS()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            managingFunctions.restart()
            pygame.quit()
            quit()
        userKey.checkForFuncitons(event)

    clock.tick(graphics.gameGraphics.tfps)


