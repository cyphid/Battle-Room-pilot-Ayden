# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#FF0000",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    if my_head["x"] == 0:
        is_move_safe["left"] = False

    elif my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    elif my_head["y"] == 0:
        is_move_safe["down"] = False

    elif my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    
    
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes or itself
    all_snakes = game_state['board']['snakes']  # Get all snakes on the board
    for snake in all_snakes:
        for segment in snake['body']:
            # Check if a segment is directly adjacent to your head
            if segment['x'] == my_head['x'] and segment['y'] == my_head['y'] + 1:
                is_move_safe['up'] = False
            if segment['x'] == my_head['x'] and segment['y'] == my_head['y'] - 1:
                is_move_safe['down'] = False
            if segment['x'] == my_head['x'] + 1 and segment['y'] == my_head['y']:
                is_move_safe['right'] = False
            if segment['x'] == my_head['x'] - 1 and segment['y'] == my_head['y']:
                is_move_safe['left'] = False
  
    
    

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    heads = []
    tails = []
    
    for snake in game_state['board']['snakes']:
        if snake['body'][0] != game_state['you']['body'][0]:
            heads.append(snake['body'][0])
            tails.append(snake['body'][-1])
    
        for segment in snake['body']:
            if segment != game_state['you']['body'][0]:
                if segment == game_state['you']['body'][1]:
                    tails.append(segment)
                    break
      
    possible_moves = []
    head = game_state['you']['body'][0]
    
    for move in ["up", "down", "left", "right"]:
        if move == "up":
            next_pos = {"x": head['x'], "y": head['y'] + 1}
        elif move == "down":
            next_pos = {"x": head['x'], "y": head['y'] - 1}
        elif move == "left":
            next_pos = {"x": head['x'] - 1, "y": head['y']}
        elif move == "right":
            next_pos = {"x": head['x'] + 1, "y": head['y']}
    
        if next_pos in heads:
            continue
    
        if next_pos not in tails or len(tails) == 0:
            possible_moves.append(move)
    
    if len(possible_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    best_move = ''
    min_dist = float('inf')
    
    for move in possible_moves:
        if move == "up":
            next_pos = {"x": head['x'], "y": head['y'] + 1}
        elif move == "down":
            next_pos = {"x": head['x'], "y": head['y'] - 1}
        elif move == "left":
            next_pos = {"x": head['x'] - 1, "y": head['y']}
        elif move == "right":
            next_pos = {"x": head['x'] + 1, "y": head['y']}
        
        dist = abs(food[0]['x'] - next_pos['x']) + abs(food[0]['y'] - next_pos['y'])
      
        if dist < min_dist:
            min_dist = dist
            best_move = move
    
    if best_move in safe_moves:
      print(f"MOVE {game_state['turn']}: {best_move}")
      return {"move": best_move}
    else:
      print(f"MOVE {game_state['turn']}: {random.choice(safe_moves)}")
      return {"move": random.choice(safe_moves)}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
