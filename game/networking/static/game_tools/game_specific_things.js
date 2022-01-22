// player object
class Player{
    constructor(body, gun, code){
        this.x = body.x;
        this.y = body.y;
        this.body = body;
        this.gun = gun;
        this.state = "stable";
        this.code = code;
    }
    shoot(direction){
        this.gun.shoot(direction);
    }
    move(move){
        this.body.move(move);
        this.gun.move(move);
    }
}

// gun obejct
class Gun{
    constructor(player, gun_shape){
        this.gun_shape = gun_shape;
        this.player = player;
        this.bullets = [];
    }
    shoot(direction){
        // do it later
    }
    move(move){
        this.gun_shape.move(move);
    }
}

// bullet object
class Bullet{
    constructor(player, bullet_shape, direction, speed){
        this.bullet_shape = bullet_shape;
        this.player = player;
        this.direction = direction;
        this.speed = speed;
    }
    move(move){
        this.gun_shape.move(move);
    }
    moving_bullet(){
        // do it later
    }

}


// moving right animation object, add the animate function to the game loop
class MovingRightAnimation{
    constructor(player, speed, block, animation_list){
        this.player = player;
        this.speed = speed;
        this.initial_speed = speed;
        this.block = block;
        this.where = 0;
        this.stage = 1;
        this.animation_list = animation_list;
        this.type = "move right";
    }

    animate(){
        if (this.where > (2*this.block)/3){
            this.stage = 2;
        }

        if (this.stage == 1){
            this.speed += 0.04;
        }
        else if (this.stage == 2){
            this.speed -= 0.04;
        }
        this.player.move([this.speed, 0]);
        this.where += this.speed

        if (this.where >= this.block){
            this.player.move([this.block-this.where, 0]);

            if (this.player.state == "move right"){
                this.stage = 1;
                this.speed = this.initial_speed;
                this.where = 0;
            }
            else{
                window.counter = 0;
                this.animation_list.splice(this.animation_list.indexOf(this), 1);
                if (this.player.state == "move left"){
                    var new_animation = new MovingLeftAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if (this.player.state == "move up"){
                    var new_animation = new MovingUpAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if(this.player.state == "move down"){
                    var new_animation = new MovingDownAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
            }
        }

    }

}


// moving left animation object, add the animate function to the game loop
class MovingLeftAnimation{
    constructor(player, speed, block, animation_list){
        this.player = player;
        this.speed = speed;
        this.initial_speed = speed;
        this.block = block;
        this.where = 0;
        this.stage = 1;
        this.animation_list = animation_list;
        this.type = "move left";
    }

    animate(){
        if (this.where > (2*this.block)/3){
            this.stage = 2;
        }

        if (this.stage == 1){
            this.speed += 0.04;
        }
        else if (this.stage == 2){
            this.speed -= 0.04;
        }
        this.player.move([-this.speed, 0]);
        this.where += this.speed

        if (this.where >= this.block){
            this.player.move([-(this.block-this.where), 0]);

            if (this.player.state == "move left"){
                this.stage = 1;
                this.speed = this.initial_speed;
                this.where = 0;
            }
            else{
                window.counter = 0;
                this.animation_list.splice(this.animation_list.indexOf(this), 1);
                if (this.player.state == "move right"){
                    var new_animation = new MovingRightAnimation(this.player, this.initial_speed, this.block,this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if (this.player.state == "move up"){
                    var new_animation = new MovingUpAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if(this.player.state == "move down"){
                    var new_animation = new MovingDownAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
            }
        }

    }

}


// moving up animation object, add the animate function to the game loop
class MovingUpAnimation{
    constructor(player, speed, block, animation_list){
        this.player = player;
        this.speed = speed;
        this.initial_speed = speed;
        this.block = block;
        this.where = 0;
        this.stage = 1;
        this.animation_list = animation_list;
        this.type = "move up";
    }

    animate(){
        if (this.where > (2*this.block)/3){
            this.stage = 2;
        }

        if (this.stage == 1){
            this.speed += 0.04;
        }
        else if (this.stage == 2){
            this.speed -= 0.04;
        }
        this.player.move([0, this.speed]);
        this.where += this.speed

        if (this.where >= this.block){
            this.player.move([0, this.block-this.where]);

            if (this.player.state == "move up"){
                this.stage = 1;
                this.speed = this.initial_speed;
                this.where = 0;
            }
            else{
                window.counter = 0;
                this.animation_list.splice(this.animation_list.indexOf(this), 1);
                if (this.player.state == "move left"){
                    var new_animation = new MovingLeftAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if (this.player.state == "move right"){
                    var new_animation = new MovingRightAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if(this.player.state == "move down"){
                    var new_animation = new MovingDownAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
            }
        }

    }

}


// moving down animation object, add the animate function to the game loop
class MovingDownAnimation{
    constructor(player, speed, block, animation_list){
        this.player = player;
        this.speed = speed;
        this.initial_speed = speed;
        this.block = block;
        this.where = 0;
        this.stage = 1;
        this.animation_list = animation_list;
        this.type = "move down";
    }

    animate(){
        if (this.where > (2*this.block)/3){
            this.stage = 2;
        }

        if (this.stage == 1){
            this.speed += 0.04;
        }
        else if (this.stage == 2){
            this.speed -= 0.04;
        }
        this.player.move([0, -this.speed]);
        this.where += this.speed;

        if (this.where >= this.block){
            this.player.move([0, -(this.block-this.where)]);

            if (this.player.state == "move down"){
                this.stage = 1;
                this.speed = this.initial_speed;
                this.where = 0;
            }
            else{
                window.counter = 0;
                this.animation_list.splice(this.animation_list.indexOf(this), 1);
                if (this.player.state == "move left"){
                    var new_animation = new MovingLeftAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if (this.player.state == "move up"){
                    var new_animation = new MovingUpAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
                else if(this.player.state == "move right"){
                    var new_animation = new MovingRightAnimation(this.player, this.initial_speed, this.block, this.animation_list);
                    this.animation_list.push(new_animation);
                }
            }
        }

    }

}


// getting box position of the position
function get_box_from_pos(pos, game_block){
    var box = [parseInt(pos[0]/game_block + 1), parseInt(pos[1]/game_block + 1)];
    return box;
}

function get_player_animation(player, animation_list){
    for (let i=0; i < animation_list.length; i++){
        var animation = animation_list[i]
        if (animation.player == player){
            return animation;
        }
    }
    return false;
}

function move_in_place_x(player, game_block){
    var box = get_box_from_pos([player.body.x, player.body.y], game_block);
    var newpos = box[0] * game_block - game_block/2;
    player.move([newpos - player.body.x, 0]);
    // return newpos;
}

function move_in_place_y(player, game_block){
    var box = get_box_from_pos([player.body.x, player.body.y], game_block);
    var newpos = box[1] * game_block - game_block/2;
    player.move([0, newpos - player.body.y]);
    // return newpos;
}