print("hello")

# sudoku = [[0 for x in range(9)] for y in range(9)]
sudo_rows = []

with open('puzzle1.sudoku') as file:
    line = "_"
    while(line != ""):
        line = file.readline()
        if(line != ""):
            row = line.split(",")
            for i in range(len(row)):
                row[i] = int(row[i][0])

            sudo_rows.append(row)
file.close()

sudo_columns = []
for j in range(len(sudo_rows[0])):
    column=[]
    for i in range(len(sudo_rows)):
        column.append(sudo_rows[i][j])
    sudo_columns.append(column)

def positionNeeds(row, column, block):
    need_list = []
    for i in row:
        if (i in column) & (i in block):
            need_list.append(i)
    return need_list

#this function makes a list of the numbers that are still missing from the needed numbers 1-9
def changeToNeeds(List):
    complete = [1,2,3,4,5,6,7,8,9]
    for i in range(len(List)):
        if List[i] in complete:
            complete.remove(List[i])
    return complete

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


def constructBlock(Coordinates):
    block = []
    for j in Coordinates[1]:
        for i in Coordinates[0]:
            block.append(sudo_rows[j][i])
    return block


sudo_blocks = []
for j in range(9):
    block_range = blockNumberRange[j]  # dictionary, blockrange format [[a,b,c][d,e,f]]
    block = constructBlock(block_range)  #to make
    sudo_blocks.append(block)


sudo_rows_needs = []
for j in range(len(sudo_rows)):
    sudo_rows_needs.append(changeToNeeds(sudo_rows[j]))

sudo_columns_needs = []
for j in range(len(sudo_columns)):
    sudo_columns_needs.append(changeToNeeds(sudo_columns[j]))

sudo_blocks_needs = []
for j in range(len(sudo_blocks)):
    sudo_blocks_needs.append(changeToNeeds(sudo_blocks[j]))


# This part makes a new row list of the sudoku.
# If we can get this to repeat until sudo_rows_need is comprised of empty
# lists we can solve the easy sudoku's presumably, i cant seem to figure out the while loop for it though


new_version_rows = []
for j in range(len(sudo_rows)):
    row = []
    for i in range(len(sudo_rows[0])):
        if sudo_rows[j][i] != 0:
            row.append(sudo_rows[j][i])
        else:
            f = 0
            for k in range(len(blockNumberRange)):
                if (j in blockNumberRange[1]) & (i in blockNumberRange[0]):
                    f = k
            possibilities = positionNeeds(sudo_rows_needs[j], sudo_columns_needs[i], sudo_blocks_needs[f])
            possibility_number = len(positionNeeds(sudo_rows_needs[j], sudo_columns_needs[i], sudo_blocks_needs[f]))
            if(possibility_number<2)&(possibility_number>0):
                row.append(possibilities[0])
            else:
                row.append(sudo_rows[j][i])
    new_version_rows.append(row)

print(sudo_rows)
print(sudo_columns)
print(sudo_blocks)
print(sudo_rows_needs)
print(sudo_columns_needs)
print(sudo_blocks_needs)
print(new_version_rows)