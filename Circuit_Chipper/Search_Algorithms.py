# This file contains various search algorithms, they will be compared on
# speed and performance. Programs that import this class will gain access
# to all these algorithms.


# Stores the wire route, name, length and some helpful functions.
class Wire:
    'class for all wires'
    wire_length = 0
    num_wires = 0
    wires_layed = 0

    def __init__(self, grid, coordinates):
        Wire.num_wires += 1
        Wire.wires_layed += 1
        self.name = 'W' + str(Wire.num_wires)
        self.coordinates = coordinates

        for coordinate in self.coordinates:
            x = coordinate[2]
            y = coordinate[1]
            z = coordinate[0]

            Wire.wire_length += 1
            grid[z][y][x] += self.name

    def remove(self, grid):
        Wire.num_wires -= 1

        for coordinate in self.coordinates:
            x = coordinate[2]
            y = coordinate[1]
            z = coordinate[0]

            grid[z][y][x].replace(self.name, '')
            Wire.wire_length -= 1
            self.coordinates = []

    def lay(self, grid, coordinate):
        self.coordinates = coordinate
        Wire.num_wires += 1
        Wire.wires_layed += 1

        for coordinate in self.coordinates:
            x = coordinate[2]
            y = coordinate[1]
            z = coordinate[0]

            Wire.wire_length += 1
            grid[z][y][x] += self.name


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
            check += 1
            if check % 1000 == 0:
                print("takes too long")
                return False

            heuristik = len(path) - 1 + distance_heuristik(pointer, end)
            new_path = [heuristik] + path[1:] + [tuple(pointer)]

            index = 0
            while index < len(paths) and paths[index][0] >= heuristik:
                index += 1

            if index == len(paths):
                paths.append(new_path)
            else:
                paths.insert(index, new_path)

        if len(paths) == 0:
            return False

    print("Found path:", paths[-1][2:-1])
    return paths[-1][2:-1]




