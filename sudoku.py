print("hello")

# sudoku = [[0 for x in range(9)] for y in range(9)]
sudo_list = []

with open('puzzle1.sudoku') as file:
    line = "_"
    while(line != ""):
        line = file.readline()
        if(line != ""):
            row = line.split(",")
            for i in range(len(row)):
                row[i] = int(row[i][0])

            sudo_list.append(row)
file.close()

print(sudo_list)
