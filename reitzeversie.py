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

#this function makes a list of the numbers that are still missing from the needed numbers 1-9
def changeToNeeds(List):
    complete = [1,2,3,4,5,6,7,8,9]
    for i in range(len(List)):
        if List[i] in complete:
            complete.remove(List[i])
    return complete

sudo_rows_needs = []
for j in range(len(sudo_rows)):
    sudo_rows_needs.append(changeToNeeds(sudo_rows[j]))

sudo_columns_needs = []
for j in range(len(sudo_columns)):
    sudo_columns_needs.append(changeToNeeds(sudo_columns[j]))

print(sudo_rows)
print(sudo_columns)
print(sudo_rows_needs)
print(sudo_columns_needs)

