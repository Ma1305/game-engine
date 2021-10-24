import pygame
import game.main
import game.graphics as graphics
import game.manager as manager

clock = manager.game_loop.clock = pygame.time.Clock()


while True:
    # drawing graphics
    for game_graphics in graphics.game_graphics_list:
        game_graphics.draw_background()
        game_graphics.draw()
    if manager.game_loop.main_game_graphics:
        manager.game_loop.screen.blit(manager.game_loop.main_game_graphics.screen.screen, (0, 0))
        pygame.display.update()

    for game_graphics in graphics.game_graphics_list:
        game_graphics.run_loopers()
        for event in pygame.event.get():
            game_graphics.on_input(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    clock.tick(manager.game_loop.fps)
