# This Algorithm calculates how "expensive" it is to lay a wire. Then it lays
# wires from most expensive to least expensive. It does this by laying the wire
# as close to the boundaries as possible.

import matplotlib.pyplot as plt
import math
from random import randint
from random import seed
import netlists


#
class Grid:
    def __init__(self, print_n, netlist):
        self.x = 0
        self.y = 0
        self.z = 0

        self.nodes = self.set_nodes(print_n)
        self.wires = self.set_wires(netlist)

    def __del__(self):
        for wire in self.wires:
            del wire
        for node in self.nodes:
            del node

    def set_nodes(self, print_n):
        nodes = {}

        with open(print_n) as file:
            line = file.readline()

            line = line.split()
            self.x = int(line[0])
            self.y = int(line[1])
            self.z = int(line[2])

            for z in range(self.z):
                for y in range(self.y):
                    for x in range(self.x):
                        nodes[(z, y, x)] = Node((z, y, x), self)

            # Set all gates in the correct nodes.
            line = file.readline()
            Gate.num_gates = 0
            while line:
                line = line.replace("(", "").replace(")", "").replace(",", "")
                line = line.split(" ")

                coordinate = (int(line[3]), int(line[2]), int(line[1]))
                del nodes[coordinate]
                gate = Gate(coordinate, self)
                nodes[coordinate] = gate
                nodes[gate.num] = gate

                line = file.readline()

        file.close()
        return nodes

    def set_wires(self, netlist):
        wires = []
        for connection in netlist:
            start_node = self.nodes[connection[0]]
            end_node = self.nodes[connection[1]]

            wire = Wire(self, [], start_node, end_node)
            wires.append(wire)
            self.nodes[connection[0]].gets(wire)
            self.nodes[connection[1]].gets(wire)
        return wires

    def print(self):
        print_grid = [[[self.nodes[(z, y, x)].objects
                        for x in range(self.x)]
                       for y in range(self.y)]
                      for z in range(self.z)]

        print()
        print("This is a grid")
        for layer in print_grid:
            for row in layer:
                print(row)
            print()


#
class Wire:
    num = 0
    layed = 0
    heat = 0

    def __init__(self, grid, coordinates, start, end):
        Wire.num += 1
        self.name = 'W' + str(Wire.num)
        self.coordinates = coordinates
        self.start = start
        self.end = end
        self.grid = grid

    def __repr__(self):
        return self.name

    def __del__(self):
        Wire.num -= 1
        self.remove()

    def lay(self, coordinates):
        if type(coordinates) == list:
            coordinates = tuple(coordinates)

        Wire.layed += 1
        nodes = self.grid.nodes

        for coordinate in coordinates:
            if type(coordinate) == list:
                coordinate = tuple(coordinate)
            nodes[coordinate].add(self)

        self.coordinates = coordinates

    def remove(self):
        nodes = self.grid.nodes

        for coordinate in self.coordinates:
            nodes[coordinate].remove(self)

    def man_dis(self, start=False, end=False):
        if type(start) == Node or type(start) == Gate:
            start = start.coordinate
        elif not start:
            start = self.start.coordinate

        if type(end) == Node or type(end) == Gate:
            end = end.coordinate
        if not end:
            end = self.end.coordinate
        man_distance = 0

        for i in range(len(start)):
            distance = start[i] - end[i]
            man_distance += abs(distance)

        return man_distance

    def a_star(self, lay=False, base=False, start=False, end=False):
        if type(end) == tuple:
            end = self.grid.nodes[end]
        elif not end:
            end = self.end
        if type(start) == tuple:
            start = self.grid.nodes[start]
        if not start:
            start = self.start

        tries = 0
        paths = [[self.man_dis(), start.coordinate]]

        while paths and self.man_dis(start=paths[-1][-1], end=end) > 1:
            path = paths.pop()
            tries += 1

            for move in self.grid.nodes[path[-1]].neighbours(end=end, empty=True):
                move = tuple(move.coordinate)

                if base and move[0] > 0:
                    continue

                heuristik = len(path) + self.man_dis(start=move)
                new_path = [heuristik] + path[1:] + [move]

                if tries > 100000:
                    return []

                index = 0
                while index < len(paths) and paths[index][0] >= heuristik:
                    index += 1
                paths.insert(index, new_path)

        if lay and paths:
            self.lay(paths[-1][2:])

        if paths:
            return paths[-1][2:]
        return []

    def a_star_cost(self):
        cost = len(self.start.neighbours(gates=True, end=self.end))\
               + len(self.end.neighbours(gates=True, end=self.start))

        for coordinate in self.a_star(base=True):
            node = self.grid.nodes[coordinate]
            cost += len(node.neighbours(gates=True))

        if self.name == 'W40':
            print(self.a_star(base=True))

        return cost

    def a_star_wall(self, start, wall, lay=False):
        if type(start) == tuple:
            start = self.grid.nodes[start]
        tries = 0
        paths = [[start.wall_dis(wall), start.coordinate]]
        max_dis = 0

        while paths and self.grid.nodes[paths[-1][-1]].wall_dis(wall) > max_dis:
            path = paths.pop()
            tries += 1

            for move in self.grid.nodes[path[-1]].neighbours(empty=True):
                move = tuple(move.coordinate)

                heuristik = len(path) + self.grid.nodes[move].wall_dis(wall)
                new_path = [heuristik] + path[1:] + [move]

                if len(new_path) > 2 * start.wall_dis(wall) + 1:
                    paths = [[start.wall_dis(wall), start.coordinate]]
                    max_dis += 1
                    continue

                index = 0
                while index < len(paths) and paths[index][0] >= heuristik:
                    index += 1
                paths.insert(index, new_path)

        if lay and paths:
            self.lay(paths[-1][2:])

        if paths:
            return paths[-1][2:]
        return []

    def connect(self):
        path = []
        to_connect = []

        for gate in [self.start, self.end]:
            wall = gate.nearest_wall()

            for coordinate in self.a_star_wall(gate, wall):
                path.append(coordinate)

            for coordinate in self.a_star_wall(path[-1], 'up'):
                path.append(coordinate)

            to_connect.append(path[-1])

        extra = self.a_star(start=to_connect[0], end=to_connect[1])
        if extra:
            for coordinate in extra:
                path.append(coordinate)
        self.lay(path)


#
class Node:
    def __init__(self, coordinate, grid):
        self.objects = []
        self.coordinate = coordinate
        self.heat = 0
        self.grid = grid

    def __repr__(self):
        return 'Node ' + str(self.coordinate)

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    def neighbours(self, gates=False, end=False, empty=False):
        position = self.coordinate
        moves = ((position[0] + 1, position[1], position[2]),
                 (position[0] - 1, position[1], position[2]),
                 (position[0], position[1] + 1, position[2]),
                 (position[0], position[1] - 1, position[2]),
                 (position[0], position[1], position[2] + 1),
                 (position[0], position[1], position[2] - 1),)
        neighbour = []

        for move in moves:
            if move in self.grid.nodes:
                node = self.grid.nodes[move]

                if gates and type(node) == Gate:
                    neighbour.append(node)
                elif empty and not node.objects:
                    neighbour.append(node)
                elif not gates and not empty:
                    neighbour.append(node)

                if end and node == end:
                    neighbour = neighbour[:-1]

        return neighbour

    def wall_dis(self, wall):
        if wall == 'north':
            return self.coordinate[1]
        if wall == 'south':
            return self.grid.y - 1 - self.coordinate[1]
        if wall == 'east':
            return self.grid.x - 1 - self.coordinate[2]
        if wall == 'west':
            return self.coordinate[2]
        if wall == 'up':
            return self.grid.z - 1 - self.coordinate[0]


#
class Gate(Node):
    num = 0
    heat = 0

    def __init__(self, coordinate, grid):
        super().__init__(coordinate, grid)
        Gate.num += 1
        self.num = Gate.num
        self.name = "G" + str(Gate.num)
        self.busy = []
        self.objects = [self]

    def __repr__(self):
        return self.name

    def __del__(self):
        Gate.num -= 1

    def gets(self, wire):
        self.busy.append(wire)

    def busyness(self):
        return len(self.busy)

    def nearest_wall(self):
        y = self.coordinate[1]
        x = self.coordinate[2]

        x_value = x - (self.grid.x / 2)
        y_value = y - (self.grid.y / 2)

        if abs(x_value) > abs(y_value):
            if x_value > 0:
                return 'east'
            else:
                return 'west'
        else:
            if y_value > 0:
                return 'south'
            else:
                return 'north'


def a_star(wires):
    if type(wires) == Wire:
        wires = [wires]

    for wire in wires:
        print(wire)
        wire.a_star(lay=True)


chip = Grid('print_1', netlists.netlist_1)
chip.wires.sort(key=lambda wire: (wire.a_star_cost(), wire.man_dis()), reverse=True)
print(chip.wires)

man = 0
for wire in chip.wires:
    print(wire)
    wire.connect()
    chip.print()
print()
print(Wire.num)
print(man)

# a_star(chip.wires)
# chip.print()
