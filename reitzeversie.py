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

blockNumberRange = {
    0: [[0, 1, 2], [0, 1, 2]],
    1: [[3, 4, 5], [0, 1, 2]],
    2: [[6, 7, 8], [0, 1, 2]],
    3: [[0, 1, 2], [3, 4, 5]],
    4: [[3, 4, 5], [3, 4, 5]],
    5: [[6, 7, 8], [3, 4, 5]],
    6: [[0, 1, 2], [6, 7, 8]],
    7: [[3, 4, 5], [6, 7, 8]],
    8: [[6, 7, 8], [6, 7, 8]]
}

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


print(positionNeeds([2,4],[1,2,3,4],[2,3,4]))

print(sudo_rows)
print(sudo_columns)
print(sudo_blocks)
print(sudo_rows_needs)
print(sudo_columns_needs)
print(sudo_blocks_needs)

