# This file contains a list of functions shared by most other files.

length = 0


#
def move_north(grid, position, wire):
    global length
    x = position[2]
    y = position[1] - 1
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move_east(grid, position, wire):
    global length
    x = position[2] + 1
    y = position[1]
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move_south(grid, position, wire):
    global length
    x = position[2]
    y = position[1] + 1
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move_west(grid, position, wire):
    global length
    x = position[2] - 1
    y = position[1]
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move_up(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] + 1

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move_down(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] - 1

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


#
def move(grid, direction, position, wire):
    if direction == 'north':
        return move_north(grid, position, wire)
    elif direction == 'east':
        return move_east(grid, position, wire)
    elif direction == 'south':
        return move_south(grid, position, wire)
    elif direction == 'west':
        return move_west(grid, position, wire)
    elif direction == 'up':
        return move_up(grid, position, wire)
    elif direction == 'down':
        return move_down(grid, position, wire)
