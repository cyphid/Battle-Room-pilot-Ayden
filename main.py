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


    # ... The code before this remains unchanged

    # Detect head-to-head collision possibilities
    my_head = game_state['you']['body'][0]
    my_length = game_state['you']['length']

    # Check the neighbouring positions of the snake's head
    possible_moves = {
        "up": {"x": my_head['x'], "y": my_head['y'] + 1},
        "down": {"x": my_head['x'], "y": my_head['y'] - 1},
        "left": {"x": my_head['x'] - 1, "y": my_head['y']},
        "right": {"x": my_head['x'] + 1, "y": my_head['y']}
    }

    # Look for other snake heads
    for snake in game_state['board']['snakes']:
        if snake['id'] == game_state['you']['id']:
            continue  # Skip checking against our own snake's head

        other_head = snake['head']
        other_length = snake['length']

        # Consider all potential moves of the other snake's head
        other_possible_moves = [
            {"x": other_head['x'] + 1, "y": other_head['y']},    # right
            {"x": other_head['x'] - 1, "y": other_head['y']},    # left
            {"x": other_head['x'], "y": other_head['y'] + 1},    # up
            {"x": other_head['x'], "y": other_head['y'] - 1},    # down
            # Diagonals
            {"x": other_head['x'] + 1, "y": other_head['y'] + 1},  # up-right
            {"x": other_head['x'] - 1, "y": other_head['y'] + 1},  # up-left
            {"x": other_head['x'] + 1, "y": other_head['y'] - 1},  # down-right
            {"x": other_head['x'] - 1, "y": other_head['y'] - 1},  # down-left
        ]

        # Check each of our possible moves
        for my_move, my_new_head in possible_moves.items():
            # If that move is already determined to be not safe, skip
            if not is_move_safe[my_move]:
                continue

            # Check if the other snake could move to the same square
            if my_new_head in other_possible_moves:
                if other_length >= my_length:  # Other snake is bigger, treat as unsafe
                    is_move_safe[my_move] = False
                elif other_length < my_length:  # Other snake is smaller, can be aggressive
                    # Decide if you want to move towards a smaller snake for a potential elimination
                    # Or keep this as a safe move depending on your strategy
                    pass  # Add your logic here
    
    
    my_head = game_state['you']['body'][0]
    my_length = game_state['you']['length']

    # Empty spaces between your snake's head and another snake's head means a potential collision
    # Check two steps away in all directions
    positions_two_steps_away = {
        "up": {"x": my_head['x'], "y": my_head['y'] + 2},
        "down": {"x": my_head['x'], "y": my_head['y'] - 2},
        "left": {"x": my_head['x'] - 2, "y": my_head['y']},
        "right": {"x": my_head['x'] + 2, "y": my_head['y']}
    }

    # Look for other snake heads that are one space away (meaning they could move to collide)
    for snake in game_state['board']['snakes']:
        if snake['id'] == game_state['you']['id']:
            continue  # Skip our own snake

        other_head = snake['head']
        other_length = snake['length']

        # Consider the move other snakes could make to reach a space one step from our head
        for move, position in positions_two_steps_away.items():
            if not is_move_safe[move]:  # If already unsafe, skip
                continue

            # Check if there's an enemy snake's head that could move into that position
            if (abs(position['x'] - other_head['x']) <= 1) and \
               (abs(position['y'] - other_head['y']) <= 1):
                if other_length >= my_length:  # Other snake is equal or larger, don't risk collision
                    is_move_safe[move] = False
                else:  # Other snake is smaller, we could possibly take it out
                    # Here you may choose to be aggressive or just keep this as a possible move
                    pass  # Add your strategy logic for aggressive play here
    
    
    # Current position of our snake's head
    my_head = game_state['you']['body'][0]
    my_length = game_state['you']['length']

    # Get the other snakes
    other_snakes = [snake for snake in game_state['board']['snakes'] if snake['id'] != game_state['you']['id']]

    # Check the positions one space away diagonally from our head
    diagonal_threats = [
        {"x": my_head['x'] - 1, "y": my_head['y'] - 1},  # Up-left
        {"x": my_head['x'] + 1, "y": my_head['y'] - 1},  # Up-right
        {"x": my_head['x'] - 1, "y": my_head['y'] + 1},  # Down-left
        {"x": my_head['x'] + 1, "y": my_head['y'] + 1},  # Down-right
    ]

    # Loop over each other snake's head
    for other_snake in other_snakes:
        other_head = other_snake['head']
        other_length = other_snake['length']

        # Calculate danger zones for each snake
        danger_zones = [
            {"x": other_head['x'] - 1, "y": other_head['y'] - 1},  # Up-left
            {"x": other_head['x'] + 1, "y": other_head['y'] - 1},  # Up-right
            {"x": other_head['x'] - 1, "y": other_head['y'] + 1},  # Down-left
            {"x": other_head['x'] + 1, "y": other_head['y'] + 1},  # Down-right
        ]

        # Compare danger zones to our next potential head positions
        for move, next_pos in possible_moves.items():
            if next_pos in danger_zones:
                # If this snake is bigger, we should be more cautious
                if other_length >= my_length:
                    is_move_safe[move] = False
                # Optional: you could include else block here to enable aggressive behavior
                # towards smaller snakes

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
  
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

