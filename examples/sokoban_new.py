from bppy import *
import itertools
from algorithms.q_learning import *
#import pygame
import time

must_finish = "must_finish"
state = "state"
pygame_settings = {
    "display": False
}
map_settings = {}


def action_to_new_location(action, i, j):
    if action == "Up":
        return i - 1, j
    if action == "Down":
        return i + 1, j
    if action == "Left":
        return i, j - 1
    if action == "Right":
        return i, j + 1


def event_to_new_location(event):
    return action_to_new_location(action=event.name, **event.data)


def event_to_2_steps_trajectory(event):
    i, j = event_to_new_location(event)
    return event_to_new_location(BEvent(event.name, {"i": i, "j": j}))


def new_location_to_events(i, j):
    return [BEvent("Up", {"i": i+1, "j": j}),
            BEvent("Down", {"i": i-1, "j": j}),
            BEvent("Left", {"i": i, "j": j+1}),
            BEvent("Right", {"i": i, "j": j-1})]


def is_adjacent(l1, l2):
    terms = list()
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]+1)
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]-1)
    terms.append(l1[0] == l2[0]+1 and l1[1] == l2[1])
    terms.append(l1[0] == l2[0]-1 and l1[1] == l2[1])
    return sum(terms) == 1


def find_adjacent_objects(list_1, list_2):
    return [(l1, l2) for l1 in list_1 for l2 in list_2 if is_adjacent(l1, l2)]

def find_adjacent_boxes(location, l):
    return [(location, l2) for l2 in l if is_adjacent(location, l2)]


def block_action(neighbors_list):
    def predicate(event):
        p1 = event_to_new_location(event)
        p2 = event_to_2_steps_trajectory(event)
        return (p1, p2) in neighbors_list or (p2, p1) in neighbors_list
    return predicate


@b_thread
def player(i, j, globals):
    directions = ["Up", "Down", "Left", "Right"]
    while True:
        e = yield {request: [BEvent(d, {"i": i, "j": j}) for d in directions], state: str(i)+"_"+str(j)}
        i, j = event_to_new_location(e)

@b_thread
def wall(globals):
    global walls_list
    block_list = list(itertools.chain(*[new_location_to_events(i, j) for i, j in globals["walls_list"]]))  # use event_to_new_location(e)
    yield {block: block_list}

@b_thread
def boxes():
    global box_list, walls_list, target_list
    while True:
        neighbors_list = find_adjacent_objects(box_list, walls_list) + \
                         find_adjacent_objects(box_list, box_list)
        double_object_movement = EventSet(block_action(neighbors_list))
        box_list_state = "_".join([str(i) for b in box_list for i in b])
        all_targets_full = sorted(box_list) == sorted(target_list)
        e = yield {block: double_object_movement, waitFor: All(), state: box_list_state, must_finish: not all_targets_full}
        new_player_location = event_to_new_location(e)
        if new_player_location in box_list:
            new_box_location = event_to_2_steps_trajectory(e)
            box_list.remove(new_player_location)
            box_list.append(new_box_location)

@b_thread
def box(i, j, globals):
    first_time = True
    while True:
        neighbors_list = find_adjacent_boxes((i, j), globals["walls_list"]) + \
                         find_adjacent_boxes((i, j), globals["box_list"])
        double_object_movement = EventSet(block_action(neighbors_list))
        box_state = str(i) + "_" + str(j)
        box_in_target = (i, j) in globals["target_list"]
        e = yield {block: double_object_movement, waitFor: All(), state: box_state,
                   must_finish: (not box_in_target) and (not first_time)}
        first_time = False
        new_player_location = event_to_new_location(e)
        if new_player_location == (i, j):
            new_box_location = event_to_2_steps_trajectory(e)
            globals["box_list"].remove(new_player_location)
            globals["box_list"].append(new_box_location)
            i, j = new_box_location

@b_thread
def aux():
    yield {waitFor: All(), state: "I"}
    while True:
        yield {waitFor: EventSet(lambda e: False), state: "S"}



# @b_thread
# def map_printer(map):
#     if pygame_settings["display"]:
#
#         main_surface = pygame.display.set_mode((32 * len(map[0]), 32 * len(map)))
#         count = 0
#         while True:
#             # Look for an event from keyboard, mouse, joystick, etc.
#             ev = pygame.event.poll()
#             if ev.type == pygame.QUIT:  # Window close button clicked?
#                 break
#             # Completely redraw the surface, starting with background
#             main_surface.fill((255, 255, 255))
#             for i in range(len(map)):
#                 for j in range(len(map[i])):
#                     # Copy our image to the surface, at this (x,y) posn
#                     main_surface.blit(map_dict[map[i][j]], (j * 32, i * 32))
#             # Now that everything is drawn, put it on display!
#             pygame.display.flip()
#             time.sleep(0.3)
#             #print(count)
#             count += 1
#
#             e = yield {waitFor: All()}
#
#             map = ",".join(map).replace("a", " ").split(",")
#             map = ",".join(map).replace("A", "t").split(",")
#             i, j = event_to_new_location(e)
#             if map[i][j] == "b" or map[i][j] == "B":
#                 i2, j2 = event_to_2_steps_trajectory(e)
#                 if map[i2][j2] == "t":
#                     map[i2] = map[i2][:j2] + "B" + map[i2][j2 + 1:]
#                 else:
#                     map[i2] = map[i2][:j2] + "b" + map[i2][j2 + 1:]
#                 if map[i][j] == "b":
#                     map[i] = map[i][:j] + "a" + map[i][j+1:]
#                 else:
#                     map[i] = map[i][:j] + "A" + map[i][j + 1:]
#             elif map[i][j] == "t":
#                 map[i] = map[i][:j] + "A" + map[i][j + 1:]
#             else:
#                 map[i] = map[i][:j] + "a" + map[i][j + 1:]
#     else:
#         yield {waitFor: All()}
#

# run
def find(map, ch):
    return [(i, j) for i, row in enumerate(map) for j, c in enumerate(row) if c == ch]



# import os
# directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))
# map_dict = {
#     " ": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/floor.png")), (32,32)),
#     "X": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/wall.png")), (32,32)),
#     "b": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/box.png")), (32,32)),
#     "B": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/box_on_target.png")), (32,32)),
#     "a": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/player.png")), (32,32)),
#     "A": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/player_on_target.png")), (32,32)),
#     "t": pygame.transform.scale(pygame.image.load(os.path.join(directory, "sokoban_pygame/box_target.png")), (32,32))
# }


def init_bprogram():
    globals = {}
    map = map_settings["map"]
    globals["walls_list"] = find(map, "X")
    globals["box_list"] = find(map, "b") + find(map, "B")
    empty_target_list = find(map, "t") + find(map, "A")
    full_target_list = find(map, "B")
    globals["target_list"] = empty_target_list + full_target_list
    player_locations = find(map, "a") + find(map, "A")
    player_location = player_locations[0]

    bthreads_list = [aux()] + [player(*player_location, globals), wall(globals)] + [box(*l, globals) for l in globals["box_list"] ]
    return BProgram(bthreads=bthreads_list, event_selection_strategy=SimpleEventSelectionStrategy())

