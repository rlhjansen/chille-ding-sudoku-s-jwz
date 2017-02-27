# an array containing the coordinate sets for different blocks
# the first element for example contains the coordinate set for
# a block of row 0 column 0,1,2 row 1 column 0,1,2 row 2 column 0,1,2
blockNumberRange = [
    [[0, 1, 2], [0, 1, 2]],
    [[3, 4, 5], [0, 1, 2]],
    [[6, 7, 8], [0, 1, 2]],
    [[0, 1, 2], [3, 4, 5]],
    [[3, 4, 5], [3, 4, 5]],
    [[6, 7, 8], [3, 4, 5]],
    [[0, 1, 2], [6, 7, 8]],
    [[3, 4, 5], [6, 7, 8]],
    [[6, 7, 8], [6, 7, 8]]
]


# this function returns a single block by combining the coordinates
# to construct a list that makes up a block
def constructBlock(Coordinates, RowList):
    block = []

    for j in Coordinates[1]:
        for i in Coordinates[0]:
            block.append(RowList[j][i])
    return block


# This function checks if the input list of lists contains no zeroes
# if it doesn't contain any it returns true, otherwise false
def containsNoZero(List):
    for i in range(len(List)):
        for j in range(len(List[i])):
            current_number = List[i][j]
            if 0 == current_number:
                return False
    return True


# Return the coordinates of the first zero after previous_zero.
def findNextZero(row_list, previous_zero):
    if previous_zero[1] == 8:
        x = previous_zero[0] + 1
        y = 0
    else:
        x = previous_zero[0]
        y = previous_zero[1] + 1

    for j in range(y, 9):
        if row_list[x][j] == 0:
            return [x, j]

    for i in range(x + 1, 9):
        for j in range(0, 9):
            if row_list[i][j] == 0:
                return [i, j]

    return False


# Returns a list with the row, column and block in which the input coordinates are in.
def coordinateToLists(coordinates, row_list, column_list, block_list):
    coor_list = []
    coor_list.append(row_list[coordinates[0]])
    coor_list.append(column_list[coordinates[1]])

    for i in range(9):
        if coordinates[0] in blockNumberRange[i][1] and coordinates[1] in blockNumberRange[i][0]:
            coor_list.append(block_list[i])

    return coor_list


# This function opens the sudoku file and returns a list of rows
def openSudoku(string):
    sudo_rows = []
    with open(string) as file:
        line = "_"
        while(line != ""):
            line = file.readline()
            if(line != ""):
                row = line.split(",")
                for i in range(len(row)):
                    row[i] = int(row[i][0])
                sudo_rows.append(row)
    file.close()
    return sudo_rows


# Return all numbers that are not present in the input list.
def missingNumbers(list):
    missing_list = []

    for i in range(1,10):
        if not i in list:
            missing_list.append(i)

    return missing_list


# Return a list of allowed numbers that can be filled in the place of the zero.
def positionAllows(coor_list):
    allow_list = []
    row_missing = missingNumbers(coor_list[0])

    for i in row_missing:
        if (not i in coor_list[1]) & (not i in coor_list[2]):
            allow_list.append(i)

    return allow_list


# Make a list of all blocks in the sudoku.
def createBlockList(row_list):
    sudo_blocks = []

    for j in range(9):
        block_range = blockNumberRange[j]  # dictionary, blockrange format [[a,b,c][d,e,f]]
        block = constructBlock(block_range, row_list)  #to make
        sudo_blocks.append(block)

    return sudo_blocks


# Make a list of all columns in the sudoku.
def createColumnList(row_list):
    sudo_columns = []

    for j in range(len(row_list[0])):
        column = []

        for i in range(len(row_list)):
            column.append(row_list[i][j])

        sudo_columns.append(column)

    return sudo_columns


# Find all easy zeros and replace them with valid values.
def replaceEasyZeros(row_list, stafe_spate):
    zero_replaced = True

    while (not containsNoZero(row_list)) and zero_replaced == True:
        zero_replaced = False
        coor_zero = [0, 0]
        column_list = createColumnList(row_list)
        block_list = createBlockList(row_list)

        while findNextZero(row_list, coor_zero) != False:
            coor_zero = findNextZero(row_list, coor_zero)
            list_zero = coordinateToLists(coor_zero, row_list, column_list, block_list)
            allow_zero = positionAllows(list_zero)

            if len(allow_zero) == 1:
                row_list[coor_zero[0]][coor_zero[1]] = allow_zero[0]
                zero_replaced = True
            elif len(allow_zero) == 0:


    return row_list


#
def replaceHardZeros(row_list, stafe_spate):



#
def solveSudoku():
    stafe_spate = []
    stafe_spate.append(openSudoku("puzzle3.sudoku"))

    while not containsNoZero(stafe_spate[-1]):
        stafe_spate = replaceEasyZeros(stafe_spate)
        stafe_spate = replaceHardZeros(stafe_spate)
    for i in range(9):
        print(row_list[i])

solveSudoku()
