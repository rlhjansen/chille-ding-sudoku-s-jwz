#
#
#

import netlists
import queue as Q
from random import shuffle
from random import randint
import matplotlib.pyplot as plt



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

    def reset(self):
        Wire.num = 0
        Wire.layed = 0
        Gate.num = 0

        for wire in self.wires:
            wire.remove()

    def set_nodes(self, print_n):
        nodes = {}

        file = open(print_n)
        file.seek(0, 0)
        line = file.readline()

        line = line.split()
        self.x = int(line[0])
        self.y = int(line[1])
        self.z = int(line[2]) + 10

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
        gates = sorted(self.gates, key=lambda gate: gate.busyness(), reverse=True)

        for gate in gates:
            for wire in gate.busy:
                lift(wire, 0, init=True)

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

    def lay(self, coordinates):
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
        return len(self.busy) + len(self.neighbours(gates=True))


#
def wires_to_lay(layed_wires, grid):
    to_lay = []

    for wire in grid.wires:
        if not (wire in layed_wires):
            to_lay.append(wire)

    return to_lay


#
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
def elevator(grid, show=False):
    height = -1
    layed = []
    can_lay = []

    while len(layed) < len(grid.wires) and height < grid.z - 1:
        height += 1

        for wire in wires_to_lay(layed, grid):
            wire.remove()
            start_end = lift(wire, height)
            can_lay.append((wire, start_end[0], start_end[1]))

        while can_lay:
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


#
def total_manhat(wires):
    length = 0

    for wire in wires:
        length += wire.man_dis()

    return length


#
def total_length(wires):
    length = 0

    for wire in wires:
        length += len(wire.coordinates)

    return length

#
def mutate_order(order):
    i_1 = randint(0, len(order) - 1)
    i_2 = randint(0, len(order) - 1)
    wire_1 = order[i_1]
    wire_2 = order[i_2]

    mut_order = []
    index = 0
    while index < len(order):
        if index == i_1:
            mut_order.append(wire_2)
        elif index == i_2:
            mut_order.append(wire_1)
        else:
            mut_order.append(order[index])

        index += 1

    return mut_order

#
def hill_climber(net, repeats=5000):
    print('netlist', net)
    p = ''

    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    shuffle(grid.wires)

    best_order = []
    for wire in grid.wires:
        best_order.append(wire)

    best_height = elevator(grid)
    best_length = total_length(grid.wires)

    print('Order 1 =', best_order)
    print('Height =', best_height)
    print('length =', best_length)
    print()
    grid.reset()

    for rep in range(repeats - 1):
        grid.reserve_gates()
        new_order = mutate_order(best_order)
        grid.wires = new_order
        new_height = elevator(grid)
        new_length = total_length(grid.wires)

        print('Order', str(rep), '=', new_order)
        print('Height =', new_height)
        print('Length =', new_length)

        if new_height <= 9 and new_length <= best_length:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('shorter length!')
        elif best_height >= 9 and new_height < best_height:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('lower height!')

        print()
        grid.reset()

    print('Best Order =', best_order)
    print('Best Height =', best_height)
    print('Best Length =', best_length)
    print('Min Length =', total_manhat(best_order))
    print()

def alt_mutate_order(order, mutations):
    currentmut = order
    for _ in range(mutations):
        i_1 = randint(0, len(order) - 1)
        i_2 = randint(0, len(order) - 1)
        while i_1 == i_2:
            i_2 = randint(0, len(order) - 1)
        wire_1 = currentmut[i_1]
        wire_2 = currentmut[i_2]

        mut_order = []
        index = 0
        while index < len(order):
            if index == i_1:
                mut_order.append(wire_2)
            elif index == i_2:
                mut_order.append(wire_1)
            else:
                mut_order.append(currentmut[index])

            index += 1
        currentmut = mut_order

    return currentmut

def alt_hill_climber(net, repeats):
    output_file = open("output.txt", "w")
    print('netlist', net)
    p = ''


    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    shuffle(grid.wires)

    best_order = []
    for wire in grid.wires:
        best_order.append(wire)

    best_height = elevator(grid)
    best_length = total_length(grid.wires)

    print('Order 1 =', best_order)
    print('Height =', best_height)
    print('length =', best_length)
    print()
    grid.reset()
    count = 0
    mutations = 1
    for rep in range(repeats - 1):
        count += 1
        if count > 20*mutations**2:
            count = 0
            mutations +=1

        grid.reserve_gates()
        new_order = alt_mutate_order(best_order, mutations)
        grid.wires = new_order
        new_height = elevator(grid)
        new_length = total_length(grid.wires)

        print('Order', str(rep), '=', new_order)
        print('Height =', new_height)
        print('Length =', new_length)
        output_file.write("[" + str(new_order) + ", " + str(new_length) + "]\n")
        if new_length < best_length:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('shorter length!')
            count -= 20*(mutations-1)**2
            mutations -= 1
            if count<0 or mutations <1:
                count = 0
                mutations = 1
        elif new_length == best_length and new_height < best_height:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('shorter length!')
            count -= 20*(mutations-1)**2
            mutations -= 1
            if count < 0 or mutations < 1:
                count = 0
                mutations = 1
        print()
        grid.reset()
    print('Best Order =', best_order)
    print('Best Height =', best_height)
    print('Best Length =', best_length)
    print('Min Length =', total_manhat(best_order))
    print()
    output_file.close()


#batchsize/survivesize must be a whole number

def decreasing_shuffle_climber(net, batchsize=480, survivesize=80, shuffle_decrement=1, start_mutate=8):
    complete_lengthlist = []
    generationlist = []
    generationcounter = 0
    print('netlist', net)
    p = ''

    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    orderlist = [None] * batchsize
    resultlist = [None] * batchsize
    grid.reset()
    for i in range(batchsize):
        shuffle(grid.wires)
        order = []
        for wire in grid.wires:
            order.append(wire)
        orderlist[i] = order

    for i in range(batchsize):
        grid.reserve_gates()
        grid.wires = orderlist[i]
        height = elevator(grid)
        wire_length = total_length(grid.wires)
        resultlist[i] = wire_length
        print("Height is: ", height)
        print("Wire_length", wire_length)
        print("manhattan distance:", total_manhat(grid.wires))
        grid.reset()
    complete_lengthlist.extend(resultlist)
    generationlist.append(len(complete_lengthlist))
    resultlist, orderlist = (list(x) for x in zip(
        *sorted(zip(resultlist, orderlist), key=lambda pair: pair[0])))
    if start_mutate == 0:
        mutations = len(grid.wires)
    else:
        mutations = start_mutate
    while mutations > 0:
        generationcounter += 1
        cumulative_wirelength = 0
        for i in range(int(batchsize/survivesize)):
            if i == 0:
                for j in range(survivesize):
                    cumulative_wirelength += resultlist[j]
            else:
                for j in range(survivesize):
                    grid.reserve_gates()
                    orderlist[i*survivesize+j] = alt_mutate_order(orderlist[j],mutations)
                    grid.wires = orderlist[i*survivesize+j]
                    height = elevator(grid)
                    wire_length = total_length(grid.wires)
                    resultlist[i] = wire_length
                    cumulative_wirelength += wire_length
                    print("Height is: ", height)
                    print("Wire_length", wire_length)
                    print("manhattan distance:", total_manhat(grid.wires), "generation:", generationcounter)
                    resultlist[i*survivesize+j] = total_length(grid.wires)
                    grid.reset()
            complete_lengthlist.extend(resultlist)
            generationlist.append(generationlist[-1]+len(complete_lengthlist))
            resultlist, orderlist = (list(x) for x in zip(
            *sorted(zip(resultlist, orderlist), key=lambda pair: pair[0])))
        mutations -= shuffle_decrement
        print("generationaverage is:", round(cumulative_wirelength/batchsize))
    grid.reserve_gates()
    grid.wires=orderlist[0]
    best_height = elevator(grid)
    best_length = total_length(grid.wires)
    print('Best Order =', orderlist[0])
    print('Best Height =', best_height)
    print('Best Length =', best_length)
    print('Min Length =', total_manhat(orderlist[0]))
    print()
    plt.plot(complete_lengthlist)
    for xc in generationlist:
        plt.axvline(x=xc, color='r')
    plt.ylabel('length')
    plt.xlabel('iterations')
    plt.show()


def decreasing_mutations(net, batchsize=480, survivesize=80, shuffle_decrement=1, start_mutate=8):
    complete_lengthlist = []
    generationlist = []
    height_is_satisfied = 0
    generationcounter = 0
    print('netlist', net)
    p = ''

    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    orderlist = [None] * batchsize
    resultlist = [None] * batchsize
    grid.reset()
    for i in range(batchsize):
        shuffle(grid.wires)
        order = []
        for wire in grid.wires:
            order.append(wire)
        orderlist[i] = order

    for i in range(batchsize):
        grid.reserve_gates()
        grid.wires = orderlist[i]
        height = elevator(grid)
        if height < 9 and height_is_satisfied == 0:
            height_is_satisfied = i
        wire_length = total_length(grid.wires)
        resultlist[i] = wire_length
        print("Height is: ", height)
        print("Wire_length", wire_length)
        print("manhattan distance:", total_manhat(grid.wires))
        grid.reset()
    complete_lengthlist.extend(resultlist)
    generationlist.append(len(complete_lengthlist))
    resultlist, orderlist = (list(x) for x in zip(
        *sorted(zip(resultlist, orderlist), key=lambda pair: pair[0])))
    if start_mutate == 0:
        mutations = len(grid.wires)
    else:
        mutations = start_mutate
    while mutations > 0:
        generationcounter += 1
        cumulative_wirelength = 0
        for i in range(int(batchsize/survivesize)):
            if i == 0:
                for j in range(survivesize):
                    cumulative_wirelength += resultlist[j]
            else:
                for j in range(survivesize):
                    grid.reserve_gates()
                    orderlist[i*survivesize+j] = alt_mutate_order(orderlist[j],mutations)
                    grid.wires = orderlist[i*survivesize+j]
                    height = elevator(grid)
                    if height < 9 and height_is_satisfied == 0:
                        height_is_satisfied = i
                    wire_length = total_length(grid.wires)
                    resultlist[i] = wire_length
                    cumulative_wirelength += wire_length
                    print("Height is: ", height)
                    print("Wire_length", wire_length)
                    print("manhattan distance:", total_manhat(grid.wires), "generation:", generationcounter)
                    resultlist[i*survivesize+j] = total_length(grid.wires)
                    grid.reset()
            complete_lengthlist.extend(resultlist)
            generationlist.append(generationlist[-1]+len(complete_lengthlist))
            resultlist, orderlist = (list(x) for x in zip(
            *sorted(zip(resultlist, orderlist), key=lambda pair: pair[0])))
        mutations -= shuffle_decrement
        print("generationaverage is:", round(cumulative_wirelength/batchsize))
    grid.reserve_gates()
    grid.wires=orderlist[0]
    best_height = elevator(grid)
    best_length = total_length(grid.wires)
    print('Best Order =', orderlist[0])
    print('Best Height =', best_height)
    print('Best Length =', best_length)
    print('Min Length =', total_manhat(orderlist[0]))
    print()
    return [complete_lengthlist, generationlist, height_is_satisfied, orderlist[0], best_height, best_length]

def hill_climber_data(net, repeats=5000):
    complete_lengthlist = []
    height_is_satisfied = 0
    print('netlist', net)
    p = ''

    if net < 4:
        p = 'print_1'
    else:
        p = 'print_2'

    grid = eval("Grid(\'" + p + "\', netlists.netlist_" + str(net) + ")")
    shuffle(grid.wires)

    best_order = []
    for wire in grid.wires:
        best_order.append(wire)

    best_height = elevator(grid)
    best_length = total_length(grid.wires)

    print('Order 1 =', best_order)
    print('Height =', best_height)
    print('length =', best_length)
    print()
    grid.reset()

    for rep in range(repeats - 1):
        grid.reserve_gates()
        new_order = mutate_order(best_order)
        grid.wires = new_order
        new_height = elevator(grid)
        new_length = total_length(grid.wires)
        complete_lengthlist.append(new_length)
        if new_height < 9 and height_is_satisfied == 0:
            height_is_satisfied = rep
        print('Order', str(rep), '=', new_order)
        print('Height =', new_height)
        print('Length =', new_length)

        if new_height <= 9 and new_length <= best_length:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('shorter length!')
        elif best_height >= 9 and new_height < best_height:
            best_order = new_order
            best_height = new_height
            best_length = new_length
            print('lower height!')

        print()
        grid.reset()

    print('Best Order =', best_order)
    print('Best Height =', best_height)
    print('Best Length =', best_length)
    print('Min Length =', total_manhat(best_order))
    print()
    return [complete_lengthlist, height_is_satisfied, best_order, best_height, best_length]


decreasing_shuffle_climber(6, 200, 40, 2, 12)

#def gather_decrshffle_climber():

#hill_climber(1, 2500)

