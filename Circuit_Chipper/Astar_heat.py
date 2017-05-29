#
#
#

import netlists
import queue as Q
import random as rn


class Grid:
    def __init__(self, print_n, netlist):
        self.x = 0
        self.y = 0
        self.z = 0

        self.nodes = self.set_nodes(print_n)
        self.wires = self.set_wires(netlist)
        self.gates = []

        for i in range(Gate.num):
            gate = self.nodes[i + 1]

            self.gates.append(gate)
            gate.add_heat(Gate.heat)
        self.gates = sorted(self.gates, key=lambda gate: gate.busyness(), reverse=True)

    def reset(self, reserve=False):
        Wire.num = 0
        Wire.layed = 0
        Gate.num = 0

        for wire in self.wires:
            wire.remove()
        if reserve:
            self.reserve_gates()

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

    def reserve_gates(self):
        for gate in self.gates:
            for wire in gate.busy:
                lift(wire, 0, init=True)

    def set_heat(self, w, g):
        old_heat = Gate.heat

        Wire.heat = w
        Gate.heat = g

        for gate in self.gates:
            gate.remove_heat(old_heat)
            gate.add_heat(g)

    def print(self, z_layer=False, heat=False):
        print_grid = []

        for z in range(self.z):
            print_grid.append([])
            for y in range(self.y):
                print_grid[-1].append([])
                for x in range(self.x):
                    node = self.nodes[(z, y, x)]

                    if heat:
                        print_grid[-1][-1].append(node.heat)
                    else:
                        print_grid[-1][-1].append(node.objects)

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


#
class Wire:
    num = 0
    layed = 0
    heat = []

    def __init__(self, grid, coordinates, start, end):
        Wire.num += 1
        self.name = 'W' + str(Wire.num)
        self.coordinates = coordinates
        self.start = start
        self.end = end
        self.grid = grid

    def __repr__(self):
        return self.name

    def lay(self, coordinates):
        Wire.layed += 1
        nodes = self.grid.nodes

        for coordinate in coordinates:
            if type(coordinate) == list:
                coordinate = tuple(coordinate)

            nodes[coordinate].add(self)
            nodes[coordinate].add_heat(Wire.heat)

        self.coordinates = coordinates

    def remove(self):
        nodes = self.grid.nodes

        for coordinate in self.coordinates:
            nodes[coordinate].remove(self)
            nodes[coordinate].remove_heat(Wire.heat)

        self.coordinates = []

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

    def a_star(self, y=False, start=False, end=False):
        if type(end) == tuple:
            end = self.grid.nodes[end]
        elif not end:
            end = self.end
        if type(start) == tuple:
            start = self.grid.nodes[start]
        elif not start:
            start = self.start

        paths = Q.PriorityQueue()
        paths.put([self.man_dis(), 0, start.coordinate])
        nodes_visited = {start.coordinate}
        path = [self.man_dis(), 0, start.coordinate]

        while not paths.empty() and path[-1] != end.coordinate:
            path = paths.get()

            for move in self.grid.nodes[path[-1]].neighbours(end=end, empty=True, wire=self):
                move = tuple(move.coordinate)

                if (type(y) == int and move[0] > y) or move in nodes_visited:
                    continue

                heat_cost = path[1] + self.grid.nodes[move].heat
                heuristik = len(path) + self.man_dis(start=move, end=end) + heat_cost

                new_path = [heuristik, heat_cost] + path[2:] + [move]
                nodes_visited.add(move)

                paths.put(new_path)

        if paths.empty():
            return False

        return path[3:-1]

    def a_star_cost(self, y=False, length=True, start=False, end=False):
        cost = len(self.start.neighbours(gates=True, end=self.end))\
               + len(self.end.neighbours(gates=True, end=self.start))

        path = self.a_star(y=y, start=start, end=end)
        if not path:
            return 1000

        for coordinate in path:
            node = self.grid.nodes[coordinate]
            cost += len(node.neighbours(gates=True))
            if length:
                cost += 1

        return cost


#
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

    def add_heat(self, heat_list):
        last_nodes = [list(self.coordinate)]
        directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0],
                      [0, -1, 0], [0, 0, 1], [0, 0, -1]]

        for length in range(len(heat_list)):
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

                    if (x + y + z < length) or (
                        next_node in next_nodes) or tuple(
                            next_node) not in self.grid.nodes:
                        continue
                    next_nodes.append(next_node)

            for next_node in next_nodes:
                self.grid.nodes[tuple(next_node)].heat += heat_list[length - 1]

            last_nodes = next_nodes

    def remove_heat(self, heat_list):
        last_nodes = [list(self.coordinate)]
        directions = [[1, 0, 0], [-1, 0, 0], [0, 1, 0],
                      [0, -1, 0], [0, 0, 1], [0, 0, -1]]

        for length in range(len(heat_list)):
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

                    if (x + y + z < length) or (
                        next_node in next_nodes) or tuple(
                            next_node) not in self.grid.nodes:
                        continue
                    next_nodes.append(next_node)

            for next_node in next_nodes:
                self.grid.nodes[tuple(next_node)].heat -= heat_list[length - 1]

            last_nodes = next_nodes


#
class Gate(Node):
    num = 0
    heat = []

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
        return len(self.busy) + len(self.neighbours(gates=True))


#
def a_star_all(wires):
    layed = 0
    not_layed = []

    for wire in wires:
        wire.remove()
        route = wire.a_star()

        if route != False:
            layed += 1
            wire.lay(route)
        else:
            not_layed.append(wire)

    return layed, not_layed


#
def mutate_heat(heat_list):
    new_list = list(heat_list)

    mut = rn.randint(0, 2)
    if new_list == [] or mut == 0:
        new_heat = rn.randint(0, 20)
        new_list.append(new_heat)
    elif mut == 1:
        del new_list[-1]
    elif mut == 2:
        index = rn.randrange(0, len(heat_list))
        new_list[index] = rn.randint(0, 20)

    return tuple(new_list)


#
def hill_heat(print_n, netlist, iterations):
    grid = Grid(print_n, netlist)
    rn.shuffle(grid.wires)
    grid.reserve_gates()
    best_heat = ()
    best_layed = 0
    past_heats = set(best_heat)

    for _ in range(iterations):
        new_heat = mutate_heat(best_heat)
        while new_heat in past_heats:
            new_heat = mutate_heat(new_heat)

        grid.set_heat([], new_heat)

        layed = a_star_all(grid.wires)
        new_layed = layed[0]
        past_heats.add(new_heat)

        if layed[1] and new_layed >= best_layed:
            best_layed = new_layed
            best_heat = new_heat
            print('better layed:', new_layed)
            print('not layed:', layed[1])
            print('new heat:', best_heat)

        elif layed[1] == [] and (len(new_heat) < len(best_heat) or
            (sum(new_heat) <= sum(best_heat) and
             len(new_heat) <= len(best_heat))):

            best_layed = new_layed
            best_heat = new_heat
            print('better layed:', new_layed)
            print('new heat:', best_heat)

        grid.reset(reserve=True)

    print('best_layed =', best_layed)
    print('best heat =', best_heat)
    return best_heat


#
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


#
def total_length(wires):
    length = 0

    for wire in wires:
        length += len(wire.coordinates)

    return length


#
def a_star_heat(grid):
    not_layed = 0

    for wire in grid.wires:
        wire.remove()
        route = wire.a_star()

        if route == False:
            not_layed += 1
        else:
            wire.lay(route)

    return not_layed


hill_heat('print_1', netlists.netlist_3, 10000)

if False:
    grid = Grid('print_2', netlists.netlist_4)
    grid.set_heat([], [0, 0, 1])
    grid.print(heat=True)
    grid.reserve_gates()
    print(a_star_all(grid.wires))
    grid.print()
