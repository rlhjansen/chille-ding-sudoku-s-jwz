# This file contains a list of functions shared by most other files.

length = 0


# Move one north, then append the name of the wire to that place in the grid.
def move_north(grid, position, wire):
    global length
    x = position[2]
    y = position[1] - 1
    z = position[0]

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Move one east, then append the name of the wire to that place.
def move_east(grid, position, wire):
    global length
    x = position[2] + 1
    y = position[1]
    z = position[0]

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Move one south, then append the name of the wire.
def move_south(grid, position, wire):
    global length
    x = position[2]
    y = position[1] + 1
    z = position[0]

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Move west, then append the name of the wire.
def move_west(grid, position, wire):
    global length
    x = position[2] - 1
    y = position[1]
    z = position[0]

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Move up, append the name of the wire.
def move_up(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] + 1

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Move down, append the wire.
def move_down(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] - 1

    grid[z][y][x].append(wire)
    length += 1
    return [z, y, x]


# Determine which direction you need to move.
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
