import second_game
import first_game
import manager
import pygame
import user_input as ui
import graphics


# setting up the screen and main graphics
manager.game_loop.make_screen(1000, 700)
manager.game_loop.set_main_game_graphics(first_game.game_graphics)


# switching games on screen
def switch_screen(event):
    global second_game
    print("hi")
    if event.key == pygame.K_SPACE:

        if manager.game_loop.main_game_graphics == first_game.game_graphics:
            manager.game_loop.set_main_game_graphics(second_game.game_graphics)
            for inp in first_game.game_graphics.on_input_list:
                print(inp.name, inp.state)

        elif manager.game_loop.main_game_graphics == second_game.game_graphics:
            print("switching again")
            manager.game_loop.set_main_game_graphics(first_game.game_graphics)

    elif event.key == pygame.K_n:
        import second_game
        print(len(graphics.game_graphics_list))


f_input_func = ui.InputFunc("switch screen", pygame.KEYDOWN, switch_screen, pass_event=True)
first_game.game_graphics.add_input_func(f_input_func)

