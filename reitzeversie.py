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

print(sudo_list)