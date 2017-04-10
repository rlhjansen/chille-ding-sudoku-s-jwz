# This file contains various search algorithms, they will be compared on
# speed and performance. Programs that import this class will gain access
# to all these algorithms.
from random import randint


# print the chip.
def print_grid(grid):
    for i in range(len(grid)):
        grid_layer = grid[i]

        for j in range(len(grid_layer)):
            print(grid_layer[j])

        print("\n")


# Stores the wire route, name, length and some helpful functions.
class Wire:
    'class for all wires'
    wire_length = 0
    wires_layed = 0

    def __init__(self, grid, coordinates, start, end):
        self.name = 'W' + str(1 + Wire.wires_layed) + '.'
        self.coordinates = coordinates
        Wire.lay(self, grid, coordinates)
        self.conflicts = Wire.num_conflicts(self, grid)
        self.start = start
        self.end = end

    def remove(self, grid):
        for coordinate in self.coordinates:
            x = coordinate[2]
            y = coordinate[1]
            z = coordinate[0]

            grid[z][y][x] = grid[z][y][x].replace(self.name, '')
            Wire.wire_length -= 1

        self.coordinates = []

    def lay(self, grid, coordinate):
        self.coordinates = coordinate
        Wire.wires_layed += 1

        for coordinate in self.coordinates:
            x = coordinate[2]
            y = coordinate[1]
            z = coordinate[0]

            Wire.wire_length += 1
            grid[z][y][x] += self.name

    def num_conflicts(self, grid):
        num_conflicts = 0

        for coordinate in self.coordinates:
            node = grid[coordinate[0]][coordinate[1]][coordinate[2]]

            if node != self.name:
                num_conflicts += 1

        return num_conflicts


# Calculate manhattan distance between two points
def distance_heuristik(start, end):
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    z = abs(start[2] - end[2])

    return x + y + z


# Check if a wire can be placed on the coordinates
def legal_position(position, grid, end):
    if position[0] > 7 or position[0] < 0:
        return False
    elif position[1] >= len(grid[0]) or position[1] < 0:
        return False
    elif position[2] >= len(grid[0][0]) or position[2] < 0:
        return False
    elif grid[position[0]][position[1]][position[2]] == '':
        return True
    elif (position[0], position[1], position[2]) == end:
        return True
    return False


# Returns the amount of overlapping wires/gates in the grid.
def num_conflicts(grid):
    conflicts = 0
    for layer in grid:
        for row in layer:
            for node in row:
                num_wires = 0

                for character in node:
                    if character.isalpha():
                        num_wires += 1

                if num_wires > 1:
                    conflicts += num_wires -1

    return conflicts


# Draw a wire from start to end with the A-star method.
def connect_wire(start, end, grid):

    paths = [[distance_heuristik(start, end), start]]
    directions = ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0),
                  (-1, 0, 0))
    check = 0 # This is when A-star takes too long about 1 line

    while paths[-1][-1] != end:
        path = paths.pop()

        for direction in directions:
            pointer = list(path[-1])

            for i in range(len(pointer)):
                pointer[i] += direction[i]

            if not(legal_position(pointer, grid, end)) or tuple(pointer) in path:
                continue

            heuristik = len(path) - 1 + distance_heuristik(pointer, end)
            new_path = [heuristik] + path[1:] + [tuple(pointer)]

            check += 1
            if check == 400:
                return False


            index = 0
            while index < len(paths) and paths[index][0] >= heuristik:
                index += 1

            if index == len(paths):
                paths.append(new_path)
            else:
                paths.insert(index, new_path)

        if len(paths) == 0:
            return False

    return paths[-1][2:-1]


#
def choose_wires(num, wires):
    wires_chosen = []

    while len(wires_chosen) < num:
        index = randint(1, len(wires)) - 1

        if index not in wires_chosen:
            wires_chosen.append(wires[index])

    return wires_chosen


#
def revert_mutation(grid, wires, coordinates):
    for index in range(len(wires)):
        Wire.remove(wires[index], grid)
        Wire.lay(wires[index], grid, coordinates[index])


#
def mutate_wires(grid, wires):
    old_coordinates = []

    for wire in wires:
        old_coordinates.append(wire.coordinates)
        Wire.remove(wire, grid)

    for wire in wires:
        path = connect_wire(wire.start, wire.end, grid)

        if path == False:
            revert_mutation(grid, wires, old_coordinates)
            return False

        Wire.lay(wire, grid, path)

    return old_coordinates


#
def hillclimber(grid, wires):
    conflicts = num_conflicts(grid)

    while conflicts > 0:
        wires_chosen = choose_wires(2, wires)
        wire_backup = mutate_wires(grid, wires_chosen)

        if wire_backup:
            new_conflicts = num_conflicts(grid)

            if new_conflicts > conflicts:
                revert_mutation(grid, wires_chosen, wire_backup)
            else:
                conflicts = new_conflicts


