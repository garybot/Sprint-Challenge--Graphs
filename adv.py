from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
adjacency = {}
back_path = {"n": "s", "e": "w", "s": "n", "w": "e"}

def has_unexplored_exits(room):
    return "?" in adjacency[room].values()

def add_to_visited():
    # If the current room is not in the adjacency list, add it.
    if not adjacency.get(player.current_room.id):
        adjacency[player.current_room.id] = {}
        for direction in player.current_room.get_exits():
            adjacency[player.current_room.id][direction] = "?"

def move(direction):
    # travel
    last_room = player.current_room.id

    player.travel(direction)
    traversal_path.append(direction)
    
    current_room = player.current_room.id

    # update adjacency list
    adjacency[last_room][direction] = current_room
    add_to_visited()
    # if not adjacency.get(player.current_room.id):
    #     adjacency[player.current_room.id] = {}
    #     for direction in player.current_room.get_exits():
    #         adjacency[player.current_room.id][direction] = "?"
    # else:
    adjacency[current_room][back_path[direction]] = last_room

def DFS():
    while has_unexplored_exits(player.current_room.id):
        # choose an unexplored direction
        directions = player.current_room.get_exits()
        unexplored = [d for d in directions if adjacency[player.current_room.id][d] == "?"]
        direction = random.choice(unexplored)
        move(direction)

def find_unexplored():
    q = Queue()
    q.enqueue(player.current_room.id)
    visited = set()
    paths = {player.current_room.id: []}
    
    while q.size():
        current = q.dequeue()

        if has_unexplored_exits(current):
            return paths[current]

        if current not in visited:
            visited.add(current)

            for direction in adjacency[current]:
                q.enqueue(adjacency[current][direction])
                # if not paths.get(adjacency[current][direction]):
                paths[adjacency[current][direction]] = paths[current] + [direction]

def traverse():
    add_to_visited()
    while len(adjacency) < len(world.rooms):
        DFS()  # Find a dead end
        # Find an unexplored exit
        if len(adjacency) < len(world.rooms):
            path = find_unexplored()
            for direction in path:
                move(direction)

traverse()



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
