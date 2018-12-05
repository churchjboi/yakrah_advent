__author__ = "yakrah"

from argparse import ArgumentParser
from collections import namedtuple

import numpy as np


def parse_args():
    argument_parser = ArgumentParser()

    argument_parser.add_argument('--input-file', default='puzzle_input.txt')

    return argument_parser.parse_args()


def get_coordinates(left_offset, top_offset, width, height):
    coordinates = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]

    coordinates = [(x + left_offset, y+top_offset) for x, y in coordinates]
    return coordinates


def parse_grid(grid):
    grid = grid.split(' ')
    grid_id = grid[0].strip('#')
    left_offset, top_offset = grid[2].strip(':').split(',')
    width, height = grid[3].split('x')
    return grid_id, int(left_offset), int(top_offset), int(height), int(width)


def slice_it_up(grid_tuples, grid_size=1050):
    full_grid = np.zeros((grid_size, grid_size))

    for grid_tuple in grid_tuples:
        coordinates = get_coordinates(grid_tuple.l_offset, grid_tuple.t_offset, grid_tuple.width, grid_tuple.height)
        top_left, top_right, bottom_right, bottom_left = coordinates

        slice_width = top_right[0] - top_left[0]
        slice_length = bottom_left[1] - top_left[1]

        for i in range(0, slice_length+1):
            for j in range(0, slice_width+1):
                full_grid[grid_tuple.t_offset+i][grid_tuple.l_offset+j] = \
                    full_grid[grid_tuple.t_offset+i][grid_tuple.l_offset+j] + 1
    return full_grid


def slice_it_up_part_two(grid_tuples, grid_size=1050):
    full_grid = np.zeros((grid_size, grid_size))

    for grid_tuple in grid_tuples:
        coordinates = get_coordinates(grid_tuple.l_offset, grid_tuple.t_offset, grid_tuple.width, grid_tuple.height)
        top_left, top_right, bottom_right, bottom_left = coordinates

        slice_width = top_right[0] - top_left[0]
        slice_length = bottom_left[1] - top_left[1]

        for i in range(0, slice_length+1):
            for j in range(0, slice_width+1):
                full_grid[grid_tuple.t_offset+i][grid_tuple.l_offset+j] = \
                    grid_tuple.id if full_grid[grid_tuple.t_offset+i][grid_tuple.l_offset+j] == 0 else -1
    return full_grid


def get_grid_inputs(input_file):
    grid_tuple = namedtuple('GridTuple', ['id', 'l_offset', 't_offset', 'width', 'height', 'pristine_grid_count'])
    grid_tuples = []
    with open(input_file, 'r') as input_open:
        for grid in input_open:
            grid_id, l_offset, t_offset, height, width = parse_grid(grid)
            grid_tuples.append(grid_tuple(grid_id, l_offset, t_offset, width, height, float(width*height)))
    return grid_tuples


if __name__ == "__main__":
    args = parse_args()

    grid_inputs = get_grid_inputs(args.input_file)

    # P1
    solved_grid = slice_it_up(grid_inputs)
    print('The grid has {} overlaps'.format((solved_grid > 1).sum()))
    # End P1

    # P2
    grid_input_map = {int(grid_input.id): grid_input for grid_input in grid_inputs}

    more_solved_grid = slice_it_up_part_two(grid_inputs)

    unique, counts = np.unique(more_solved_grid, return_counts=True)
    grid_counts = dict(zip(unique, counts))
    del grid_counts[0]
    del grid_counts[-1]
    for grid_id, grid_count in grid_counts.items():
        if grid_input_map[int(grid_id)].pristine_grid_count == grid_count:
            print('The only pristine grid is ID #{}'.format(int(grid_id)))
    # End P2
