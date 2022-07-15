import queue
import time
from typing import List, Tuple
from grid import Grid
import pyautogui
from controller import Controller

GRID_WIDTH = 6
GRID_HEIGHT = 12
OFFSET_X = 12
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_WIDTH = 36
TILE_HEIGHT = 32
COLORS = {
    'red': (218, 120, 81),
    'blue': (0, 213, 233),
    'purple': (222, 156, 222),
    'green': (0, 171, 36),
    'yellow': (130, 108, 0)
}


def find_best_action(grid_orig: Grid) -> Tuple[int, int]:
    best_score = grid_orig.get_score()
    best_swaps = []
    action_queue = queue.PriorityQueue()
    action_queue.put((best_score, []))
    visited_states = []

    i = 0
    while i < 100 and not action_queue.empty():
        (local_score, actions) = action_queue.get()
        grid = grid_orig.clone()
        for (ax, ay) in actions:
            grid.swap(ax, ay)
            grid.exec_game_rules_all()

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH - 1):
                changes = grid.swap(x, y)
                if len(changes) == 0:
                    continue

                changes += grid.exec_game_rules_all()
                score = grid.get_score()
                if score < best_score:
                    best_score = score
                    best_swaps = actions + [(x, y)]

                if grid.get_cell_ids() not in visited_states:
                    visited_states.append(grid.get_cell_ids())
                    new_actions = actions.copy()
                    new_actions.append((x, y))
                    action_queue.put((score, new_actions))

                grid.rollback(changes)

        i += 1

    return best_swaps


def find_left_bottom_cell():
    bottom_pos = pyautogui.locateOnScreen('bottom.png', confidence=0.95)

    # Try to find a tile to determine the current offset of the grid
    offset = 100
    tile_colors = ['blue', 'green', 'purple', 'red', 'yellow']
    for color in tile_colors:
        tile = pyautogui.locateCenterOnScreen(f'tiles/{color}.png', confidence=0.9, region=(
            bottom_pos[0] - 20, bottom_pos[1] - 2 * TILE_HEIGHT, 7 * TILE_WIDTH, 2 * TILE_HEIGHT))

        if tile is None:
            continue

        delta = (bottom_pos.top - tile.y)
        if delta < offset:
            offset = delta

    if offset < .5 * TILE_HEIGHT:
        offset += TILE_HEIGHT

    print('offset', offset)

    return (bottom_pos[0] + OFFSET_X, bottom_pos[1] - offset)


if __name__ == "__main__":
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    cell_left_bottom = find_left_bottom_cell()

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pixel = pyautogui.pixel(
                int(cell_left_bottom[0]) + x * TILE_WIDTH, int(cell_left_bottom[1]) - y * TILE_HEIGHT)
            # print(pixel)
            # pyautogui.screenshot(f"tmp/{y}-{x}.png", (
            #     int(cell_left_bottom[0]) + x * TILE_WIDTH,
            #     int(cell_left_bottom[1]) - y * TILE_HEIGHT,
            #     100,
            #     100
            # ))

            smallest_dist_val = 3 * 255
            smallest_dist_col = None
            for (name, color) in COLORS.items():
                dist = abs(pixel[0] - color[0]) + abs(pixel[1] -
                                                      color[1]) + abs(pixel[2] - color[2])
                if dist < smallest_dist_val:
                    smallest_dist_val = dist
                    smallest_dist_col = name

            if smallest_dist_val < 20:
                grid.set_cell_id(x, y, smallest_dist_col)

    controller = Controller()
    grid.print()
    time_start = time.perf_counter()
    best_swaps = find_best_action(grid.clone())
    time_stop = time.perf_counter()
    print(
        f"Best swaps {best_swaps} took {time_stop - time_start:0.4f} seconds")
    for swap in best_swaps:
        grid.swap(swap[0], swap[1])
        grid.exec_game_rules_all()
        controller.move_to((swap[0], swap[1]))
        controller.swap()
    grid.print()
