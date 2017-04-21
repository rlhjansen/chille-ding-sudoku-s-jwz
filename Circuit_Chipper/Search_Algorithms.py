# This file contains various search algorithms, they will be compared on
# speed and performance. Programs that import this class will gain access
# to all these algorithms.
from random import randint
from random import seed
import netlists


# Return the path of a wire that goes manhattan distance with conflicts.
def connect_conflicting_wire(start, end):
    pointer = start
    path = []

    x_moves = start[2] - end[2]
    if x_moves < 0:
        x_direction = - 1
        x_moves = - x_moves
    else:
        x_direction = 1

    y_moves = start[1] - end[1]
    if y_moves < 0:
        y_direction = - 1
        y_moves = - y_moves
    else:
        y_direction = 1

    while x_moves != 0 or y_moves != 0:
        if y_moves == 0 or (x_moves != 0 and randint(0, 1) == 0):
            pointer = (0, pointer[1], pointer[2] - x_direction)
            x_moves -= 1
        else:
            pointer = (0, pointer[1] - y_direction, pointer[2])
            y_moves -= 1

        path.append(pointer)

    return path[:-1]


#
class Grid:
    """The class for a grid that contains Nodes"""

    def __init__(self, print):
        self.nodes = {}
        self.gates = {}
        self.wires = []

        # Make all nodes.
        with open(print) as file:
            line = file.readline()

            line = line.split()
            self.x_length = int(line[0])
            self.y_length = int(line[1])
            self.z_length = int(line[2])

            for z in range(self.z_length):
                for y in range(self.y_length):
                    for x in range(self.x_length):
                        self.nodes[(z, y, x)] = Node((z, y, x))

            # Set all gates in the correct nodes.
            line = file.readline()
            while line:
                line = line.replace("(", "").replace(")", "").replace(",", "")
                line = line.split(" ")

                coordinate = (int(line[3]), int(line[2]), int(line[1]))
                gate = Gate(coordinate)
                self.nodes[coordinate].add(gate)
                self.gates[int(line[0])] = gate

                line = file.readline()

        file.close()

    def init_wires(self, netlist):
        for connection in netlist:
            start = self.gates[connection[0]]
            end = self.gates[connection[1]]

            wire_path = connect_conflicting_wire(start.coordinate, end.coordinate)
            self.wires.append(Wire(self, wire_path, start, end))

        return self.wires

    def print(self):
        print_grid = [[[self.nodes[(z, y, x)].name()
                        for x in range(self.x_length)]
                       for y in range(self.y_length)]
                      for z in range(self.z_length)]

        print()
        print("This is a grid")
        for layer in print_grid:
            for row in layer:
                print(row)
            print()

    def print_heatmap(self):
        print_grid = [[[self.nodes[(z, y, x)].heat
                        for x in range(self.x_length)]
                       for y in range(self.y_length)]
                      for z in range(self.z_length)]

        for z in range(self.z_length):
            for y in range(self.y_length):
                for x in range(self.x_length):
                    node = self.nodes[(z, y, x)]

                    if node.objects and type(node.objects[0]) is Gate:
                        print_grid[z][y][x] = node.name()

        print("-----------------")
        print("This is a heatmap")
        for layer in print_grid:
            for row in layer:
                print(row)
            print()


# These nodes are data points that store wires, gates and the heat.
class Node:
    """Class for all nodes in the grid"""

    def __init__(self, coordinate):
        self.objects = []
        self.coordinate = coordinate
        self.heat = 0

    def add(self, object):
        self.objects.append(object)

    def remove(self, object):
        self.objects.remove(object)

    def name(self):
        name = ''

        for object in self.objects:
            name += object.name + ' '

        return name[:-1]

    def conflicts(self):
        if len(self.objects) > 1:
            return len(self.objects) - 1
        else:
            return 0

    def valid(self, end):
        if not self.objects:
            return True
        elif self.coordinate == end and type(self.objects[0]) == Gate:
            return True

        return False


# Stores the wire route, name, length and some helpful functions.
class Wire:
    """class for all wires"""
    wire_length = 0
    wires_layed = 0
    heat = 1

    def __init__(self, grid, coordinates, start, end):
        self.name = 'W' + str(1 + Wire.wires_layed)
        self.coordinates = coordinates
        Wire.lay(self, grid, coordinates)
        self.conflicts = Wire.num_conflicts(self, grid)
        self.start = start
        self.end = end

    def remove(self, grid):
        for coordinate in self.coordinates:
            grid.nodes[coordinate].remove(self)
            Wire.wire_length -= 1

        self.coordinates = []

    def lay(self, grid, coordinate):
        self.coordinates = coordinate
        Wire.wires_layed += 1

        for coordinate in self.coordinates:
            grid.nodes[coordinate].add(self)
            Wire.wire_length += 1

    def num_conflicts(self, grid):
        conflicts = 0

        for coordinate in self.coordinates:
            if grid.nodes[coordinate].conflicts() != 0:
                conflicts += 1

        return conflicts

    def __del__(self):
        Wire.wire_length = 0
        Wire.wires_layed = 0

    def length(self):
        return len(self.coordinates)


class Gate:
    """Class for all gates"""
    num_gates = 0
    heat = 2

    def __init__(self, coordinate):
        self.coordinate = coordinate
        Gate.num_gates += 1
        self.name = 'G' + str(Gate.num_gates)

    def heat_point(self, grid):
        heat = Gate.heat
        last_nodes = [list(self.coordinate)]
        directions = [[1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]

        for length in range(Gate.heat):
            length += 1
            next_nodes = []

            for node in last_nodes:
                for direction in directions:
                    next_node = [node[0] + direction[0],
                                 node[1] + direction[1],
                                 node[2] + direction[2]]

                    x = abs(self.coordinate[0] - next_node[0])
                    y = abs(self.coordinate[1] - next_node[1])
                    z = abs(self.coordinate[2] - next_node[2])

                    if (x + y + z < length) or (next_node in next_nodes) or tuple(next_node) not in grid.nodes:
                        continue
                    next_nodes.append(next_node)

            for next_node in next_nodes:
                grid.nodes[tuple(next_node)].heat += heat

            last_nodes = next_nodes
            heat -= 1


# Calculate manhattan distance between two points
def distance_heuristik(start, end):
    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])
    z = abs(start[2] - end[2])

    return x + y + z


#
def calculate_heuristik(path, pointer, end, grid):
    heuristik = distance_heuristik(pointer, end)
    manhat_distance = heuristik
    end_heat = grid.nodes[(1, end[1], end[2])].heat

    if manhat_distance < end_heat:
        heuristik -= grid.nodes[(1, end[1], end[2])].heat - manhat_distance

    heuristik += grid.nodes[pointer].heat + 1

    return heuristik


#
def calculate_Astar_heuristik(path, pointer, end, grid):
    heuristik = distance_heuristik(pointer, end)
    manhat_distance = heuristik
    end_heat = grid.nodes[(1, end[1], end[2])].heat

    if manhat_distance < end_heat:
        for heat in range(1 + grid.nodes[(1, end[1], end[2])].heat - manhat_distance):
            heuristik -= heat

    for node in path[2:]:
        heuristik += grid.nodes[node].heat + 1
    heuristik += grid.nodes[pointer].heat + 1

    return heuristik


# Check if a wire can be placed on the coordinates
def legal_position(position, grid, end):
    position = tuple(position)

    if position not in grid.nodes:
        return False
    elif not grid.nodes[position].valid(end):
        return False

    return True


# Returns the amount of overlapping wires/gates in the grid.
def num_conflicts(grid):
    conflicts = 0
    nodes = grid.nodes.values()

    for node in nodes:
        conflicts += node.conflicts()

    return conflicts


# Determines if a line is too hard to lay, and skips it for now.
def stop(tries, heuristik, manhat_distance):
    if heuristik < 1:
        return False
    elif tries > float(1/heuristik) * manhat_distance * 100:
        # print("stopped, heuristik = {} and tries is {}" .format(heuristik, tries))
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
            pointer = tuple(pointer)

            if not(legal_position(pointer, grid, end)) or pointer in path:
                continue

            heuristik = calculate_heuristik(path, pointer, end, grid)
            new_path = [heuristik] + path[1:] + [pointer]

            check += 1
            if stop(check, heuristik, distance_heuristik(start, end)):
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
    index_chosen = []

    while len(index_chosen) < num:
        index = randint(1, len(wires)) - 1

        if index not in index_chosen:
            index_chosen.append(index)

    wires_chosen = []

    for index in index_chosen:
        wires_chosen.append(wires[index])

    return wires_chosen


# Won't make conflicts when laying wires.
def mutate_wires_careful(grid, wires):
    old_coordinates = []
    paths = []

    for wire in wires:
        old_coordinates.append(wire.coordinates)
        wire.remove(grid)

    for wire in wires:
        path = connect_wire(wire.start.coordinate, wire.end.coordinate, grid)

        if path != False:
            wire.lay(grid, path)

        paths.append(path)

    if False in paths:
        for i in range(len(wires)):
            wires[i].remove(grid)
            wires[i].lay(grid, old_coordinates[i])


# Can make conflicts between mutating wires and wires that failed to mutate.
def mutate_wires_risky(grid, wires):
    old_coordinates = []

    for wire in wires:
        old_coordinates = [wire.coordinates] + old_coordinates
        wire.remove(grid)

    for wire in wires:
        path = connect_wire(wire.start.coordinate, wire.end.coordinate, grid)

        if path:
            old_coordinates.pop()
            wire.lay(grid, path)
        else:
            wire.lay(grid, old_coordinates.pop())


# Tolerates conflicts, only if there are less then before, hillclimber.
def mutate_wires_hillclimber(grid, wires):
    old_coordinates = []
    paths = []
    old_conflicts = num_conflicts(grid)

    for wire in wires:
        old_coordinates.append(wire.coordinates)
        wire.remove(grid)

    for wire in wires:
        path = connect_wire(wire.start.coordinate, wire.end.coordinate, grid)
        paths.append(path)

    for i in range(len(wires)):
        if paths[i] != False:
            wires[i].lay(grid, paths[i])
        else:
            wires[i].lay(grid, old_coordinates[i])

    if num_conflicts(grid) > old_conflicts:
        for i in range(len(wires)):
            wires[i].remove(grid)
            wires[i].lay(grid, old_coordinates[i])


#
def solve_conflicts_duo(grid, wires):
    num_tries = 0
    conflicts = num_conflicts(grid)
    num_wires = 1

    while conflicts > 0 and num_wires < 10:
        while num_tries < 1000 + num_wires * num_wires * 100:
            wires_chosen = choose_wires(num_wires, wires)
            mutate_wires_careful(grid, wires_chosen)
            new_conflicts = num_conflicts(grid)

            if new_conflicts < conflicts:
                conflicts = new_conflicts
                num_tries = 0

            num_tries += 1

        num_tries = 0
        grid.print()
        print_stats(grid)

        while num_tries < 1000 + num_wires * num_wires * 100:
            wires_chosen = choose_wires(num_wires, wires)
            mutate_wires_careful(grid, wires_chosen)
            new_conflicts = num_conflicts(grid)

            if new_conflicts < conflicts:
                conflicts = new_conflicts
                num_tries = 0

            num_tries += 1

        num_tries = 0
        grid.print()
        print_stats(grid)

        num_wires += 1


#
def solve_conflicts_solo(grid, wires):
    num_tries = 0
    conflicts = num_conflicts(grid)
    num_wires = 1

    while conflicts > 0:
        wires_chosen = choose_wires(num_wires, wires)
        mutate_wires_hillclimber(grid, wires_chosen)
        new_conflicts = num_conflicts(grid)

        if new_conflicts < conflicts:
            conflicts = new_conflicts
            num_tries = 0

        num_tries += 1
        if num_tries > 1000 + num_wires * num_wires * 100:
            num_tries = 0
            num_wires += 1
            grid.print()
            print_stats(grid)

        if num_wires > 10:
            break


def print_stats(grid):
    print("There were {} iterations."
          .format(Wire.wires_layed))
    print("The total length of the wires is {}."
          .format(Wire.wire_length))
    print("Conflicts left is:", num_conflicts(grid))


chip = Grid("print_1")
gates = chip.gates.values()
for gate in gates:
    gate.heat_point(chip)

if False:
    start = chip.gates[netlists.netlist_1[0][0]]
    end = chip.gates[netlists.netlist_1[0][1]]

    wire_path = connect_wire(start.coordinate, end.coordinate, chip)
    if wire_path:
        chip.wires.append(Wire(chip, wire_path, start, end))

if True:
    wires = chip.init_wires(netlists.netlist_3)
    solve_conflicts_solo(chip, wires)
chip.print_heatmap()
chip.print()
print_stats(chip)
