from networking.web_setup import *
from networking import networking
import main_folder.game as game
import graphics
import user_input as ui
import json
import manager


@web_socket.on("connect")
def new_connection():
    client_id = request.sid
    client = networking.Client(client_id, server, None)
    print("New Connection", client_id)
    client.send({"name": "start", "content": "it is working"})

    player = game.create_player(client)
    player.send({"command": "set_game_info", "player_radius": game.PLAYER_RADIUS, "block_size": game.BLOCK})

    msg_this_player = game.convert_player_to_dictionary(player)
    msg_this_player["command"] = "set_up_your_player"
    player.send(msg_this_player)

    player.send({"command": "set_up_camera", "zoom": 1})

    all_players = []
    for player in player.game_graphics.storage["player_list"]:
        all_players.append(game.convert_player_to_dictionary(player))

    player.send({"command": "set_up_all_players", "all_players": all_players})

    background_lines = player.game_graphics.storage["vertical_lines"] + player.game_graphics.storage["horizontal_lines"]
    background_lines_dictionaries = []
    for line in background_lines:
        background_lines_dictionaries.append(game.convert_line_to_dictionary(line))

    player.send({"command": "set_up_background_lines", "line_list": background_lines_dictionaries})
    '''
    speed = 2

    def move_player():
        player.move((-speed, 0))
    '''
    '''move_player_right = game.MovingRightAnimation(player, 1, game.BLOCK)
    move_player_left = game.MovingDownAnimation(player, 1.5, game.BLOCK)
    move_right_looper = ui.Looper("move right", move_player_left.animate)
    player.state = "move right"
    move_player_left.animate_looper = move_right_looper
    player.game_graphics.add_looper(move_right_looper)'''

    for players in player.game_graphics.storage["player_list"]:
        if players != player:
            msg = game.convert_player_to_dictionary(player)
            msg["command"] = "new player"
            players.send(msg)

    # start game
    if len(player.game_graphics.storage["player_list"]) == player.game_graphics.storage["maximum"]:
        for player in player.game_graphics.storage["player_list"]:
            player.send({"command": "start game"})
            move_player_right = game.MovingRightAnimation(player, 1.5, game.BLOCK)
            move_right_looper = ui.Looper("move right", move_player_right.animate)
            player.state = "move right"
            move_right_looper.animate_looper = move_right_looper
            player.game_graphics.add_looper(move_right_looper)
            move_player_right.animate_looper = move_right_looper
            player.game_graphics.storage["animation_list"].append(move_player_right)


        game_graphics = player.game_graphics
        game_graphics.storage["counter"] = 0

        '''def secondly_update():
            game_graphics.storage["counter"] += 1

            if game_graphics.storage["counter"] == 10:
                all_players = []
                for player in game_graphics.storage["player_list"]:
                    all_players.append(game.convert_player_to_dictionary(player))
                for player in game_graphics.storage["player_list"]:
                    print({"command": "secondly_update", "player_list": all_players})
                    player.send({"command": "secondly_update", "player_list": all_players})

            if game_graphics.storage["counter"] == manager.game_loop.fps:
                game_graphics.storage["counter"] = 0

        secondly_update_looper = ui.Looper("secondly_update", secondly_update)
        game_graphics.add_looper(secondly_update_looper)'''


@web_socket.on("message")
def handel_message(message):
    message = json.loads(message)
    command = message["command"]

    player = None
    client_code = request.sid
    for game_graphics in graphics.game_graphics_list:
        for players in game_graphics.storage["player_list"]:
            if players.client.code == client_code:
                player = players

    if command == "movement":
        player.state = "move " + message["movement"]
        for players in player.game_graphics.storage["player_list"]:
            if players != player:
                players.send({"command": "player_movement", "movement": "move " + message["movement"], "player_code": player.client.code})

    if command == "secondly_update_request":
        all_players = []
        all_animations = []
        for players in player.game_graphics.storage["player_list"]:
            all_players.append(game.convert_player_to_dictionary(players))
            all_animations.append(game.convert_animation_to_dictionary(game.get_player_animation(players, players.game_graphics.storage["animation_list"])))
        player.send({"command": "secondly_update", "player_list": all_players, "animation_list": all_animations})