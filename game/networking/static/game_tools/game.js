// setting up all the required information blah blah blah
window.game_loop_function_list = [];
window.animation_list = [];
window.game_state = "setup";
window.run_game = true;
window.socket = io();
window.shape_list = [];
window.fps = 40;
window.intervals = 1/window.fps


const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');


function send(msg){
    socket.send(JSON.stringify(msg));
}


// this game specific variables
window.player_list = [];
window.my_player = null;
window.player_radius = null;
window.player_camera = new Camera(canvas, ctx, 0, 0, 0);
window.game_block = 0;
window.counter = 1000;
window.screen_width = 600;
window.screen_height = 400;
canvas.width = window.screen_width;
canvas.height = window.screen_height;


// game loop
function game_loop(){
    // var starting_time = new Date();


    // clear screen 
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    // drawing shapes
    for (let i = 0; i < window.shape_list.length; i++){
        var shape = window.shape_list[i];
        shape.draw();
        //console.log("finished frame")
    }
    // animations
    for (let i=0; i < window.animation_list.length; i++){
        var animation = window.animation_list[i];
        animation.animate();
    }
    //loopers
    for (let i=0; i < window.game_loop_function_list.length; i++){
        var func = window.game_loop_function_list[i];
        func();
    }
    //window.requestAnimationFrame(game_loop);

    /*
    var after_action_time = new Date();
    var action_time = after_action_time.getTime() - starting_time.getTime();
    if (action_time < window.intervals){
        setTimeout(run_game_loop, window.intervals-action_time);
    }
    game_loop();*/
}
setInterval(() => {
    game_loop()
}, window.intervals*1000);
function run_game_loop(){
    requestAnimationFrame(game_loop);
}

// socket related things (I know, I'm commenting with a lot of details)
socket.on('message', function(msg) {
    msg = JSON.parse(msg);
    if (msg["command"] == "set_game_info"){
        window.player_radius = msg["player_radius"];
        window.game_block = msg["block_size"];
    }
    else if (msg["command"] == "set_up_your_player"){
        var code = msg["code"];
        var pos = msg["pos"];
        var color = msg["color"];
        var gun_shape_startpoint = msg["gun"]["shape"]["startpoint"];
        var gun_shape_endpoint = msg["gun"]["shape"]["endpoint"];
        pos = [pos[0] + window.game_block/2, pos[1] + window.game_block/2];

        var body = new Circle(ctx, pos[0]-window.game_block/2, pos[1]-window.game_block/2, window.player_radius, rgbToColor(color));
        var gun_shape = new Line(ctx, gun_shape_startpoint, gun_shape_endpoint, rgbToColor(color));
        window.shape_list.push(body);
        window.shape_list.push(gun_shape);

        var gun = new Gun(null, gun_shape);
        window.my_player = new Player(body, gun, code);
        gun.player = window.my_player;
        window.player_list.push(window.my_player);
    }
    else if (msg["command"] == "set_up_all_players"){
        var all_players = msg["all_players"];
        // adding players to player list one by one
        for (let i=0; i < all_players.length; i++){
            var player_dictionary = all_players[i];
            var code = player_dictionary["code"];
            // making sure this player is not our player, so we add our player again
            if (code != window.my_player.code){
                var pos = player_dictionary["pos"];
                pos = [pos[0] + window.game_block/2, pos[1] + window.game_block/2];
                var color = player_dictionary["color"];
                var gun_shape_startpoint = player_dictionary["gun"]["shape"]["startpoint"];
                var gun_shape_endpoint = player_dictionary["gun"]["shape"]["endpoint"];

                var body = new Circle(ctx, pos[0]-window.game_block/2, pos[1]-window.game_block/2, window.player_radius, rgbToColor(color));
                var gun_shape = new Line(ctx, gun_shape_startpoint, gun_shape_endpoint, rgbToColor(color));
                body.make_virtual(window.player_camera);
                gun_shape.make_virtual(window.player_camera);
                window.shape_list.push(body);
                window.shape_list.push(gun_shape);

                var gun = new Gun(null, gun_shape);
                var player = new Player(body, gun, code);
                gun.player = player;
                window.player_list.push(player);
            }
            else{
                window.my_player.body.make_virtual(window.player_camera);
                window.my_player.gun.gun_shape.make_virtual(window.player_camera);
            }
        }
    }
    else if (msg["command"] == "set_up_camera"){
        var zoom = msg["zoom"];
        window.player_camera = new Camera(canvas, ctx, window.my_player.x, window.my_player.y, zoom);
    }
    else if (msg["command"] == "set_up_background_lines"){
        var line_list = msg["line_list"];
        for (let i=0; i < line_list.length; i++){
            var line_info = line_list[i];
            var startPoint = line_info["startpoint"];
            var endPoint = line_info["endpoint"];
            var color = line_info["color"];
            var line = new Line(ctx, startPoint, endPoint, rgbToColor(color));
            line.make_virtual(window.player_camera);
            window.shape_list.push(line);
        }
        /*window.my_player.state = "move right";
        var speed = 1.5;
        var player_animation = new MovingDownAnimation(window.my_player, speed, window.game_block, window.animation_list);
        window.animation_list.push(player_animation);
        window.game_loop_function_list.push(fix_camera_pos);*/
    }
    else if (msg["command"] == "new player"){
        var code = msg["code"];
        var pos = msg["pos"];
        var color = msg["color"];
        var gun_shape_startpoint = msg["gun"]["shape"]["startpoint"];
        var gun_shape_endpoint = msg["gun"]["shape"]["endpoint"];
        pos = [pos[0] + window.game_block/2, pos[1] + window.game_block/2];

        var body = new Circle(ctx, pos[0]-window.game_block/2, pos[1]-window.game_block/2, window.player_radius, rgbToColor(color));
        var gun_shape = new Line(ctx, gun_shape_startpoint, gun_shape_endpoint, rgbToColor(color));
        body.make_virtual(window.player_camera);
        gun_shape.make_virtual(window.player_camera);
        window.shape_list.push(body);
        window.shape_list.push(gun_shape);

        var gun = new Gun(null, gun_shape);
        var player = new Player(body, gun, code);
        gun.player = player;
        window.player_list.push(player);
    }
    else if (msg["command"] == "start game"){
        window.game_state = "playing";
        var speed = 1.5;

        for (let i=0; i < window.player_list.length; i++){
            var player = window.player_list[i];
            player.state = "move right";
            var player_animation = new MovingRightAnimation(player, speed, window.game_block, window.animation_list);
            window.animation_list.push(player_animation);
            window.game_loop_function_list.push(fix_camera_pos);
        }
    }
    else if (msg["command"] == "player_movement"){
        var code = msg["player_code"];
        var movemnt = msg["movement"];
        for (let i=0; i < window.player_list.length; i++){
            var player = window.player_list[i];
            if (player.code == code){
                player.state = movemnt;
            }
        }
    }
    else if (msg["command"] == "secondly_update"){
        console.log("got update")
        for (let i=0; i < msg["player_list"].length; i++){
            var player = msg["player_list"][i];
            for (let c=0; c < window.player_list.length; c++){
                var client_player = window.player_list[c];
                if (client_player.code == player["code"]){
                    var client_box = get_box_from_pos([client_player.body.x, client_player.body.y], window.game_block);
                    var server_box = get_box_from_pos(player["pos"], window.game_block);
                    if (client_box[0] != server_box[0] || client_box[1] != server_box[1]){
                        console.log("fixing the positions");
                        client_player.move([player["pos"][0]-client_player.body.x, player["pos"][1]-client_player.body.y]);
                        var animation = get_player_animation(client_player, animation_list);
                        // console.log(client_player);
                        //console.log(animation);
                        //console.log(msg["animation_list"][i]["speed"], msg["animation_list"][i]["where"], msg["animation_list"][i]["stage"]);
                        animation.speed = msg["animation_list"][i]["speed"];
                        animation.where = msg["animation_list"][i]["where"];
                        animation.stage = msg["animation_list"][i]["stage"];
                        //animation.animate();
                        //console.log(animation);
                        //console.log(get_player_animation(client_player, window.animation_list));*/
                        // window.counter = 0;
                    }
                    break;
                }
            }
        }
    }
});


// game_loop();



function move_player_right(){
    var speed = 2;

    if (window.game_state != "playing"){
        return null;
    }
    window.my_player.move([-speed, 0]);
}

function fix_camera_pos(){
    window.player_camera.x = window.my_player.body.x;
    window.player_camera.y = window.my_player.body.y;
}

function secondly_update_request(){
    window.counter += 1;
    if (counter == fps/2){
        send({"command": "secondly_update_request"});
    }
}
window.game_loop_function_list.push(secondly_update_request);

function fix_player_pos(){
    for (let i=0; i < window.player_list.length; i++){
        var player = window.player_list[i];
        var animation = get_player_animation(player, window.animation_list);
        if (animation.type == player.state){
            if (player.state == "move right" || player.state == "move left"){
                move_in_place_y(player, window.game_block);
            }
            else if (player.state == "move up" || player.state == "move down"){
                move_in_place_x(player, window.game_block);
            }
        }
    }
}
window.game_loop_function_list.push(fix_player_pos);


document.addEventListener('keydown', on_keydown);

function on_keydown(event){
    if (event.which == 37){
        // left
        window.my_player.state = "move left";
        send({"command": "movement", "movement": "left"})
    }
    else if (event.which == 38){
        // up
        window.my_player.state = "move up";
        send({"command": "movement", "movement": "up"})
    }
    else if (event.which == 39){
        // right
        window.my_player.state = "move right";
        send({"command": "movement", "movement": "right"})
    }
    else if (event.which == 40){
        // down
        window.my_player.state = "move down";
        send({"command": "movement", "movement": "down"})
    }
}