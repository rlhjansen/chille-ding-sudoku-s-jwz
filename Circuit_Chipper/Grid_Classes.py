from random import randint


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

    def __init__(self, coordinate):
        self.coordinate = coordinate
        Gate.num_gates += 1
        self.name = 'G' + str(Gate.num_gates)

    def heat_point(self, grid, radius):
        heat = radius
        last_nodes = [list(self.coordinate)]
        directions = [[1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]

        for length in range(radius):
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
