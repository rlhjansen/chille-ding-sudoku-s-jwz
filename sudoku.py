print("hello")

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


# This function checks if the input list of lists contains no zeroes
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

# comment moet nog
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


