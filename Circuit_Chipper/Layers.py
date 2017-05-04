#
#
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

            wire = Wire(self, False, start_node, end_node)
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
        self.heat = Wire.heat
        self.grid = grid
        self.manhat = self.manhattan()

    def __repr__(self):
        return self.name

    def manhattan(self):
        man_distance = 0

        for i in range(len(self.start.coordinate)):
            distance = self.start.coordinate[i] - self.end.coordinate[i]
            man_distance += abs(distance)

        return man_distance


#
class Node:

    def __init__(self, coordinate, grid):
        self.objects = []
        self.coordinate = coordinate
        self.heat = 0
        self.grid = grid

    def __repr__(self):
        return 'Node ' + str(self.coordinate)

    def add(self, object):
        self.objects.append(object)


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

    def gets(self, wire):
        self.busy.append(wire)

    def busyness(self):
        return len(self.busy)



chip = Grid('print_1', netlists.netlist_1)
chip.print()
