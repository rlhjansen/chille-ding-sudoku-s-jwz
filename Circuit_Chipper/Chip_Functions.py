# This file contains a list of functions shared by most other files.

length = 0


# Move one north, then append the name of the wire to that place in the grid.
def move_north(grid, position, wire):
    global length
    x = position[2]
    y = position[1] - 1
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


# Move one east, then append the name of the wire to that place.
def move_east(grid, position, wire):
    global length
    x = position[2] + 1
    y = position[1]
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


# Move one south, then append the name of the wire.
def move_south(grid, position, wire):
    global length
    x = position[2]
    y = position[1] + 1
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


# Move west, then append the name of the wire.
def move_west(grid, position, wire):
    global length
    x = position[2] - 1
    y = position[1]
    z = position[0]

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


# Move up, append the name of the wire.
def move_up(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] + 1

    grid[z][y][x] = wire
    length += 1
    return [z, y, x]


# Move down, append the wire.
def move_down(grid, position, wire):
    global length
    x = position[2]
    y = position[1]
    z = position[0] - 1

    grid[z][y][x] = wire
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


# Remove
def remove_north(grid, position):
    global length
    x = position[2]
    y = position[1]
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z, y - 1, x]


# Move one east, then append the name of the wire to that place.
def remove_east(grid, position):
    global length
    x = position[2]
    y = position[1]
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z, y, x - 1]


# Move one south, then append the name of the wire.
def remove_south(grid, position):
    global length
    x = position[2]
    y = position[1] + 1
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z, y - 1, x]


# Move west, then append the name of the wire.
def remove_west(grid, position):
    global length
    x = position[2]
    y = position[1]
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z, y, x + 1]


# Move down, delete the name of the wire.
def remove_up(grid, position):
    global length
    x = position[2]
    y = position[1]
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z - 1, y, x]


# Move up, delete the wire.
def remove_down(grid, position):
    global length
    x = position[2]
    y = position[1]
    z = position[0]

    grid[z][y][x] = ''
    length -= 1
    return [z + 1, y, x]


# Determine which direction you need to move.
def remove(grid, direction, position):
    if direction == 'north':
        return remove_north(grid, position)
    elif direction == 'east':
        return remove_east(grid, position)
    elif direction == 'south':
        return remove_south(grid, position)
    elif direction == 'west':
        return remove_west(grid, position)
    elif direction == 'up':
        return remove_up(grid, position)
    elif direction == 'down':
        return remove_down(grid, position)


# Find for a point with the name
def get_gate(grid, gate_num):
    gate_name = 'G' + str(gate_num)

    for z in range(len(grid)):
        for y in range(len(grid[z])):
            for x in range(len(grid[z][y])):
                point = grid[z][y][x]

                if point == gate_name:
                    return [z, y, x]

    return None


#
def lay_wire(grid, start_gate, end_gate):
    start_gate = get_gate(start_gate)
    end_gate = get_gate(end_gate)


