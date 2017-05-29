# This program tries to solve the chip by using the elevator method. The
# elevator reserves places next to gates for the wires that need to connect
# those gates. Then it tries to lay all wires a-star on the base layer. If not
# all gates are connected, it lifts all unconnected wires to height = 1 and
# tries to connect them again. This process repeats until all gates are
# connected.

import netlists
import queue as Q


# This keeps track of where, which object is placed on the chip.
class Grid:
    def __init__(self, print_n, netlist):
        self.x = 0
        self.y = 0
        self.z = 0

        self.nodes = self.set_nodes(print_n)
        self.wires = self.set_wires(netlist)
        self.gates = []

        for i in range(Gate.num):
            self.gates.append(self.nodes[i + 1])
        self.reserve_gates()

    # Clean a grid for repeated use.
    def reset(self):
        Wire.num = 0
        Wire.layed = 0
        Gate.num = 0

        for wire in self.wires:
            wire.remove()

    # Part of init. Make all nodes and make all gates.
    def set_nodes(self, print_n):
        nodes = {}

        file = open(print_n)
        file.seek(0, 0)
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

    # Part of init. Make all wires.
    def set_wires(self, netlist):
        wires = []
        for connection in netlist:
            if connection[0] not in self.nodes:
                continue

            start_node = self.nodes[connection[0]]
            end_node = self.nodes[connection[1]]

            wire = Wire(self, [], start_node, end_node)
            wires.append(wire)
            self.nodes[connection[0]].gets(wire)
            self.nodes[connection[1]].gets(wire)

        return wires

    # Lay parts of wires near gates they must connect.
    def reserve_gates(self):
        gates = sorted(self.gates, key=lambda gate: gate.busyness(), reverse=True)

        for gate in gates:
            for wire in gate.busy:
                lift(wire, 0, init=True)

    # Show the content of all nodes.
    def print(self, z_layer=False):
        print_grid = [[[self.nodes[(z, y, x)].objects
                        for x in range(self.x)]
                       for y in range(self.y)]
                      for z in range(self.z)]

        print()
        print("This is a grid")
        if type(z_layer) == int:
            for row in print_grid[z_layer]:
                print(row)
            print()
        else:
            for layer in print_grid:
                for row in layer:
                    print(row)
                print()

    # Returns a list in which all the routes of all wires are.
    def all_coord(self):
        all_coords = []

        for wire in self.wires:
            coords = []

            coords.append(wire.start.coordinate)
            coords += wire.coordinates
            coords.append(wire.end.coordinate)

            all_coords.append(coords)

        return all_coords


# These connect gates. They may not intersect each other.
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

    # Put a wire on the grid.
    def lay(self, coordinates):
        Wire.layed += 1
        nodes = self.grid.nodes

        for coordinate in coordinates:
            if type(coordinate) == list:
                coordinate = tuple(coordinate)
            nodes[coordinate].add(self)

        self.coordinates = coordinates

    # Remove a wire from the grid.
    def remove(self):
        nodes = self.grid.nodes

        for coordinate in self.coordinates:
            nodes[coordinate].remove(self)

        self.coordinates = []

    # Return the length of a path without obstacles.
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

    # Return the route of a wire. Return 'False' if no route is possible.
    def a_star(self, lay=False, y=False, start=False, end=False, turn=False):
        if type(end) == tuple:
            end = self.grid.nodes[end]
        elif not end:
            end = self.end
        if type(start) == tuple:
            start = self.grid.nodes[start]
        elif not start:
            start = self.start

        paths = Q.PriorityQueue()
        paths.put([self.man_dis(), start.coordinate])
        nodes_visited = {start.coordinate}
        path = [self.man_dis(), start.coordinate]

        while not paths.empty() and path[-1] != end.coordinate:
            path = paths.get()

            for move in self.grid.nodes[path[-1]].neighbours(end=end, empty=True, wire=self):
                move = tuple(move.coordinate)

                if (type(y) == int and move[0] > y) or move in nodes_visited:
                    continue

                heuristik = len(path) + self.man_dis(start=move, end=end)
                if turn:
                    heuristik += turn_penalty(path, move)

                new_path = [heuristik] + path[1:] + [move]
                nodes_visited.add(move)

                paths.put(new_path)

        if paths.empty():
            return False

        if lay:
            self.lay(path[2:-1])
        return path[2:-1]

    # How 'expensive' is it to lay this wire using a-star.
    def a_star_cost(self, y=False, length=True, start=False, end=False):
        cost = len(self.start.neighbours(gates=True, end=self.end))\
               + len(self.end.neighbours(gates=True, end=self.start))

        path = self.a_star(y=y, start=start, end=end)
        if not path:
            return 1000

        # Cost = len(path) + len(nodes near path)
        for coordinate in path:
            node = self.grid.nodes[coordinate]
            cost += len(node.neighbours(gates=True))
            if length:
                cost += 1

        return cost


# One vertex on the grid. It can contain wires.
class Node:
    def __init__(self, coordinate, grid):
        self.objects = []
        self.coordinate = coordinate
        self.heat = 0
        self.grid = grid

    def __repr__(self):
        return 'N' + str(self.coordinate)

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    # Return all nodes neighbouring this one. You can specify which kind of
    # neighbours to return.
    def neighbours(self, gates=False, end=False, empty=False, wire=False, wires=False, init=False):
        if type(end) == tuple:
            end = self.grid.nodes[end]

        position = self.coordinate
        moves = ((position[0] + 1, position[1], position[2]),
                 (position[0] - 1, position[1], position[2]),
                 (position[0], position[1] + 1, position[2]),
                 (position[0], position[1] - 1, position[2]),
                 (position[0], position[1], position[2] + 1),
                 (position[0], position[1], position[2] - 1))
        neighbour = []

        for move in moves:
            if move in self.grid.nodes:
                node = self.grid.nodes[move]

                if gates and type(node) == Gate:
                    neighbour.append(node)
                if wires and node.objects:
                    has_wire = False
                    for object in node.objects:
                        if type(object) == Wire:
                            has_wire = True
                    if has_wire:
                        neighbour.append(node)
                elif empty and not node.objects:
                    neighbour.append(node)
                elif not gates and not empty:
                    neighbour.append(node)
                elif empty and end and node == end:
                    neighbour.append(node)
                elif empty and wire and node.objects == [wire]:
                    neighbour.append(node)

        if empty and init:
            neighbour.sort(key=lambda coord: len(coord.neighbours(gates=True)))

        return neighbour


# Gates are special nodes that are connected with each other by wires.
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

    # Tell a gate which wire is used to connect it.
    def gets(self, wire):
        self.busy.append(wire)

    # Return how crowded a gate is/will be.
    def busyness(self):
        return len(self.busy) + len(self.neighbours(gates=True))


# Return all wires that don't already connect two gates on the grid.
def wires_to_lay(layed_wires, grid):
    to_lay = []

    for wire in grid.wires:
        if not (wire in layed_wires):
            to_lay.append(wire)

    return to_lay


# Check if a wire makes a turn. Return 1 if it did, 0 if it didn't.
def turn_penalty(coordinates, pointer, kost=2):
    if len(coordinates) < 4:
        return 0
    coor_1 = coordinates[-2]
    coor_2 = coordinates[-1]

    prev_direction = None
    if coor_1[0] != coor_2[0]:
        prev_direction = 'z'
    elif coor_1[1] != coor_2[1]:
        prev_direction = 'y'
    elif coor_1[2] != coor_2[2]:
        prev_direction = 'x'

    next_direction = None
    if pointer[0] != coor_1[0]:
        next_direction = 'z'
    elif pointer[1] != coor_1[1]:
        next_direction = 'y'
    elif pointer[2] != coor_1[2]:
        next_direction = 'x'

    if prev_direction != next_direction:
        return kost
    return 0


# Extend all unlayed wires from their gates to a given height.
def lift(wire, height, init=False):
    wire.remove()
    total_path = []
    start_end = []

    for gate in [wire.start, wire.end]:
        start_nodes = gate.neighbours(empty=True, init=init)
        pointer = start_nodes[0].coordinate
        path = [pointer]

        for i in range(0, height):
            if path[0][0] != i + 1:
                path.append((i + 1, pointer[1], pointer[2]))

        start_end.append(path[-1])
        total_path += path

    wire.lay(total_path)
    return start_end


# Connect all gates using the elevator method.
def elevator(grid, show=False):
    height = -1
    layed = []
    can_lay = []

    while len(layed) < len(grid.wires) and height < grid.z - 1:
        height += 1

        # Lift all wires to the specified height.
        for wire in wires_to_lay(layed, grid):
            wire.remove()
            start_end = lift(wire, height)
            can_lay.append((wire, start_end[0], start_end[1]))

        # Try to lay each wire a-star without laying higher than the height.
        while can_lay:
            can_lay.sort(key=lambda wire_set: (wire_set[0].a_star_cost(y=height, start=wire_set[1], end=wire_set[2]), wire_set[0].man_dis()), reverse=True)
            wire_set = can_lay.pop()
            wire = wire_set[0]
            old_path = wire.coordinates
            wire.remove()
            path = wire.a_star(y=height)

            if path != False:
                wire.lay(path)
                layed.append(wire)
            else:
                wire.lay(old_path)

        if show:
            print(height, len(layed))
            grid.print(z_layer=height)

    return height + 1


# Calculate the sum of shortest possible routes from the wires.
def total_manhat(wires):
    length = 0

    for wire in wires:
        length += wire.man_dis()

    return length


# Return the number of nodes that are occupied by the wires.
def total_length(wires):
    length = 0

    for wire in wires:
        length += len(wire.coordinates)

    return length


#
def elevator_all():
    for i in range(1, 7):
        p = ''

        if i < 4:
            p = 'print_1'
        else:
            p = 'print_2'

        print('netlist', i)

        grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(i) + ")")
        grid.wires.sort(
            key=lambda wire: (wire.a_star_cost(y=False), wire.man_dis()),
            reverse=True)

        print('Height =', elevator(grid))
        print('minimal length =', total_manhat(grid.wires))
        print('result length =', total_length(grid.wires))
        print(grid.wires)
        print()

        grid.reset()
        del grid

def return_value_elevator(net):
    p = ''

    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    print('netlist', net)

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    grid.wires.sort(key=lambda wire: (wire.a_star_cost(y=False), wire.man_dis()),
            reverse=True)
    height = elevator(grid)
    totallength = total_length(grid.wires)
    print('Height =', height)
    print('minimal length =', total_manhat(grid.wires))
    print('result length =', totallength)
    print()

    return [height, totallength, grid.wires]


#elevator_all()

#print(return_value_elevator(2))

if False:
    chip = Grid('print_1', netlists.netlist_1)
    chip.wires.sort(key=lambda wire: (wire.a_star_cost(y=False), wire.man_dis()), reverse=True)

    print('layers', elevator(chip, show=True))
    print('manhat', total_manhat(chip.wires))
    print('length', total_length(chip.wires))


