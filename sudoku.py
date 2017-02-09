print("hello")

# sudoku = [[0 for x in range(9)] for y in range(9)]
sudo_list = []

with open('puzzle1.sudoku') as file:
    line = "_"
    while(line != ""):
        line = file.readline()
        if(line != ""):
            sudo_list.append(line)
file.close()

sudo_matrix = []

for i in range(9):
    row = sudo_list[i]
    numbers = row.split(",")
    fix = numbers[8]
    numbers[8] = fix[0]
    sudo_matrix.append(numbers)

print(sudo_matrix)
