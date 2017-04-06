# This file contains a list of functions shared by most other files.

length = 0


# Find for a point with the name
def get_gate(grid, gate_num):
    gate_name = 'G' + str(gate_num)

    for z in range(len(grid)):
        for y in range(len(grid[z])):
            for x in range(len(grid[z][y])):
                point = grid[z][y][x]

                if point == gate_name:
                    return [z, y, x]

    return None

