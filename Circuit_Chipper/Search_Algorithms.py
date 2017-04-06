# This file contains various search algorithms, they will be compared on
# speed and performance. Programs that import this class will gain access
# to all these algorithms.


#
class Wire:
    'class for all wires'
    wire_length = 0
    num_wires = 0

    def __init__(self, gate):
        self.pointer = gate
        Wire.num_wires += 1
        self.name = 'W' + str(Wire.num_wires)

    def move_pointer(self, direction):
        distance = 0
        for i in direction:
            if i != 0 or abs(i) != 1:
                return False
            distance += 1
        if distance != 1:
            return False

        for j in range(self.pointer):
            self.pointer[j] += direction[j]

        return self.pointer

    def lay_wire(self, grid, coordinate):
        x = coordinate[2]
        y = coordinate[1]
        z = coordinate[0]

        Wire.wire_length -= 1
        grid[z][y][x].append(self.name)

    def remove_wire(self, grid, coordinate):
        x = coordinate[2]
        y = coordinate[1]
        z = coordinate[0]

        if self.name in grid[z][y][x]:
            grid[z][y][x].replace(self.name, '')
            Wire.wire_length -= 1
            return True
        return False


# Calculate manhattan distance between two points
def distance_heuristik(start, end):
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    z = abs(start[2] - end[2])

    return x + y + z


#
def legal_position(position, grid, end):
    if position[0] > 7 or position[0] < 0:
        return False
    elif position[1] >= len(grid[0]) or position[1] < 0:
        return False
    elif position[2] >= len(grid[0][0]) or position[2] < 0:
        return False
    elif grid[position[0]][position[1]][position[2]] == '':
        return True
    elif grid[position[0]][position[1]][position[2]] == end:
        return True
    return False


#
def connect_wire(start, end, grid):
    paths = [[distance_heuristik(start, end), start]]
    directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1),
                  (0, 0, -1))

    while paths[-1][-1] != end:
        path = paths.pop()

        for direction in directions:
            pointer = list(path[-1])

            for i in range(len(pointer)):
                pointer[i] += direction[i]

            if not legal_position(pointer, grid, end):
                continue

            heuristik = len(path) - 1 + distance_heuristik(pointer, end)
            new_path = [heuristik] + path + [tuple(pointer)]

            index = 0
            while index < len(paths) and paths[index][0] > heuristik:
                index += 1

            if index == len(paths):
                paths.append(new_path)
            else:
                paths.insert(index, new_path)

        if len(paths) == 0:
            return False

    return paths[-1][2:-2]




