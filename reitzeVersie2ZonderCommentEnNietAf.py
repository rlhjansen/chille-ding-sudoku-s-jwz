
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

# goes through the entire list and returns anothr list that contains all numbers (1-9)not in the initial list.
def changeToAllows(List):
    complete = [1,2,3,4,5,6,7,8,9]
    for i in range(len(List)):
        if List[i] in complete:
            complete.remove(List[i])
    return complete

# this function returns a single block by combining the coordinates
# to construe a list that makes up a block
def constructBlock(Coordinates, RowList):
    block = []
    for j in Coordinates[1]:
        for i in Coordinates[0]:
            block.append(RowList[j][i])
    return block


# This function checks if the input list of lists contaisn no zeroes
# if it doesn't contain any it returns true, otherwise false
def containsNoZero(List):
    pls = True
    for i in range(len(List)):
        for j in range(len(List[i])):
            current_number = List[i][j]
            if 0 == current_number:
                pls = False
    return pls

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

# comment moet nog ..
def positionAllows(row, column, block, added_list):
    allow_list = []
    for i in row:
        if (i in column) & (i in block) & (not (i in added_list)):
            allow_list.append(i)
    return allow_list



# These are functions to create the lists for blocks & coloumns from the list of rows.

def createBlockList(row_list):
    sudo_blocks = []
    for j in range(9):
        block_range = blockNumberRange[j]  # dictionary, blockrange format [[a,b,c][d,e,f]]
        block = constructBlock(block_range, row_list)  #to make
        sudo_blocks.append(block)

    return sudo_blocks


def createColumnList(row_list):
    sudo_columns = []
    for j in range(len(row_list[0])):
        column = []
        for i in range(len(row_list)):
            column.append(row_list[i][j])
        sudo_columns.append(column)
    return sudo_columns


#this function takes as input either a block, column or row-list and returns a list with the possibilities for that list
def changeToAllowSudoList(list):
    sudo_allows = []
    for j in range(len(list)):
        sudo_allows.append(changeToAllows(list[j]))
    return sudo_allows



# this function is the main function that solves the sudoku
# it should probably be split into methods and made more efficient,
# to be able to solve the harder puzzles
#
def solveSudoku(string):
    row_list = openSudoku(string)
    print(row_list)
    while not (containsNoZero(row_list)):
        column_list = createColumnList(row_list)
        block_list = createBlockList(row_list)
        row_allows = changeToAllowSudoList(row_list)
        column_allows = changeToAllowSudoList(column_list)
        block_allows = changeToAllowSudoList(block_list)
        new_copy_row_list = row_list
        for j in range(len(new_copy_row_list)):
            row = []
            added_list = [] #to keep track of what is added to the current row
            for i in range(len(new_copy_row_list[0])):
                if new_copy_row_list[j][i] != 0:
                    row.append(new_copy_row_list[j][i])
                else:
                    f = 0
                    for k in range(len(blockNumberRange)):
                        if (j in blockNumberRange[k][1]) & (i in blockNumberRange[k][0]):
                            f = k
                    possibilities = positionAllows(row_allows[j], column_allows[i], block_allows[f],added_list)
                    possibility_number = len(positionAllows(row_allows[j], column_allows[i], block_allows[f], added_list))
                    if (possibility_number < 2) & (possibility_number > 0):
                        row.append(possibilities[0])
                        print(possibilities)
                        count = 0
                        added_list.append(possibilities[0])
                    else:
                        row.append(new_copy_row_list[j][i])
            #update possibilities after a row has been changed
            new_copy_row_list[j] = row
            column_list = createColumnList(new_copy_row_list)
            block_list = createBlockList(new_copy_row_list)
            row_allows = changeToAllowSudoList(new_copy_row_list)
            column_allows = changeToAllowSudoList(column_list)
            block_allows = changeToAllowSudoList(block_list)
        print(new_copy_row_list)
        if new_copy_row_list == row_list:
            count+=1        # count system used to let the function run over everything twice
            if count == 2:  # such that changes in the end affect the possibility for change in the beginning
                break       # if nothing then has changed: the program breaks.
        row_list = new_copy_row_list
    print(row_list)


solveSudoku('puzzle1.sudoku')

